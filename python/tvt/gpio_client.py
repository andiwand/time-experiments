#!/usr/bin/env python3

import time
import argparse
import socket
import wiringpi
import shared

sock = None
dest_address = None

def callback_wiringpi():
    t = shared.time()
    send(t)

def run_netlink(sock):
    try:
        while True:
            data = sock.recv(1024)
            msg_len, msg_type, flags, seq, pid = struct.unpack("=LHHLL", data[:16])
            ts_sec, ts_nsec, pin, value = struct.unpack("=LLLL", data[16:])
            t = ts_sec + ts_nsec / 1000000000.0
            send(t)
    finally:
        sock.close()

def run_polling(p):
    try:
        for line in p.stdout:
            line = line.split(" ")
            t, value = float(line[0]), int(line[1])
            send(t)
    finally:
        p.close();

def setup_wiringpi(args):
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(args.pinin, 0)
    wiringpi.pullUpDnControl(args.pinin, 1)
    wiringpi.wiringPiISR(args.pinin, wiringpi.INT_EDGE_RISING, callback_wiringpi)

def setup_netlink(args):
    # TODO: load kernel module?
    import os, socket
    SOL_NETLINK = 270
    NETLINK_ADD_MEMBERSHIP = 1
    MY_GROUP = 31
    sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, socket.NETLINK_USERSOCK)
    sock.bind((os.getpid(), MY_GROUP))
    sock.setsockopt(SOL_NETLINK, NETLINK_ADD_MEMBERSHIP, MY_GROUP)
    t = threading.Thread(target=run_netlink, args=(sock,))
    t.daemon = True
    t.start()

def setup_polling(args):
    import shlex, subprocess
    cmd = shlex.split(args.gpio_station) + [str(args.pinin), str(3)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    t = threading.Thread(target=run_polling, args=(p,))
    t.daemon = True
    t.start()

def send(t):
    global debug, sock, dest_address
    data = ("%.9f" % t).encode()
    sock.sendto(data, dest_address)
    if debug: print(t)
    return True

parser = argparse.ArgumentParser()
parser.add_argument("pinin", type=int, help="input gpio")
parser.add_argument("host", type=str, help="host to connect")
parser.add_argument("-d", "--debug", help="enable debugging", action="store_true")
parser.add_argument("-p", "--port", type=int, help="udp port (default %(default)d)", default=12345)
parser.add_argument("--gpio-netlink", help="connect to gpio-netlink.ko", action="store_true")
parser.add_argument("--gpio-polling", help="path to c gpio polling")
args = parser.parse_args()

debug = args.debug

setup_gpio = setup_wiringpi
if args.gpio_netlink: setup_gpio = setup_netlink
if args.gpio_polling: setup_gpio = setup_polling

setup_gpio(args)

dest_address = (args.host, args.port)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    while True:
        time.sleep(100)

