#!/usr/bin/env python3

# TODO: trigger gpio only from python; write to file befor sending event

import os
import time
import argparse
import socket
import threading

from timetests import shared

debug = False
last_time = None
clients = {}

def get_file(directory, address):
    global debug, clients
    if address not in clients:
        print("%s connected" % address)
        path = os.path.join(directory, address.replace(".", "_") + ".txt")
        f = open(path, "a")
        clients[address] = {"log_path": path, "log_file": f, "last_time": None}
    return clients[address]["log_file"]

def run_server(socket, directory):
    global debug, last_time, clients
    while True:
        data, addr = sock.recvfrom(1024)
        time.sleep(0.01)
        f = get_file(directory, addr[0])

        client = clients[addr[0]]
        if client["last_time"] == last_time: continue
        client["last_time"] = last_time

        f.write("%s %s\n" % (last_time, data.decode()))
        f.flush()

def run_wiringpi(args):
    import wiringpi
    global debug, last_time
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(args.pinout, 1)
    while True:
        last_time = "%.9f" % shared.time()
        wiringpi.digitalWrite(args.pinout, 1)
        time.sleep(0.00001)
        wiringpi.digitalWrite(args.pinout, 0)
        if debug: print(last_time)
        time.sleep(args.interval)

def run_gpio_station(args):
    import shlex, subprocess
    global debug, last_time
    cmd = shlex.split(args.gpio_station) + [str(args.pinout), str(args.interval)]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as p:
        for line in p.stdout:
            last_time = line.decode("us-ascii")
            if debug: print(last_time)

parser = argparse.ArgumentParser()
parser.add_argument("pinout", type=int, help="output gpio")
parser.add_argument("directory", type=str, help="data path")
parser.add_argument("-d", "--debug", help="enable debugging", action="store_true")
parser.add_argument("-p", "--port", type=int, help="udp port (default %(default)d)", default=12345)
parser.add_argument("-i", "--interval", type=float, help="signal interval (default %(default)d)", default=1)
parser.add_argument("--gpio-station", help="path to c gpio station")
args = parser.parse_args()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.port))

    debug = args.debug

    run_gpio = run_wiringpi
    if args.gpio_station: run_gpio = run_gpio_station

    t = threading.Thread(target=run_gpio, args=(args,))
    t.daemon = True
    t.start()

    run_server(sock, args.directory)
finally:
    sock.close()
    for addr in clients:
        f = clients[addr]["log_file"]
        f.close()
