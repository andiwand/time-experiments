#!/usr/bin/env python3

# TODO: add loopback gpio option (measure time on signal receive)

import os
import time
import argparse
import socket
import threading
import wiringpi
import shared

last_time = 0
clients = {}

def get_file(directory, address):
    global clients
    if address not in clients:
        print("%s connected" % address)
        path = os.path.join(directory, address.replace(".", "_") + ".txt")
        f = open(path, "a")
        clients[address] = {"log_path": path, "log_file": f, "last_time": 0}
    return clients[address]["log_file"]

def run_server(socket, directory):
    global last_time, clients
    while True:
        data, addr = sock.recvfrom(1024)
        f = get_file(directory, addr[0])
        
        client = clients[addr[0]]
        if client["last_time"] == last_time: continue
        client["last_time"] = last_time
        
        f.write("%.9f" % last_time)
        f.write(" ")
        f.write(data.decode())
        f.write("\n")
        f.flush()

def run_gpio(pinout, interval):
    global last_time
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(pinout, 1)
    while True:
        last_time = shared.time()
        wiringpi.digitalWrite(pinout, 1)
        wiringpi.digitalWrite(pinout, 0)
        time.sleep(interval)

parser = argparse.ArgumentParser()
parser.add_argument("pinout", type=int, help="output gpio")
parser.add_argument("directory", type=str, help="data path")
parser.add_argument("-p", "--port", type=int, help="set port number (default 12345)",
                    default=12345)
parser.add_argument("-i", "--interval", type=float, help="set interval (default 1)",
                    default=1)
args = parser.parse_args()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.port))

    t = threading.Thread(target=run_gpio, args=(args.pinout, args.interval))
    t.daemon = True
    t.start()

    run_server(sock, args.directory)
finally:
    sock.close()
    for addr in clients:
        f = clients[addr]["log_file"]
        f.close()

