#!/usr/bin/env python3

import time
import argparse
import socket
import wiringpi
import shared

sock = None
dest_address = None

def isr():
    global sock, dest_address
    t = shared.time()
    print("tack")
    data = ("%.9f" % t).encode()
    sock.sendto(data, dest_address)
    return True

parser = argparse.ArgumentParser()
parser.add_argument("pinin", type=int, help="input gpio")
parser.add_argument("host", type=str, help="host to connect")
parser.add_argument("-p", "--port", type=int, help="set port number (default 12345)",
                    default=12345)
args = parser.parse_args()

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(args.pinin, 0)
wiringpi.pullUpDnControl(args.pinin, 1)
wiringpi.wiringPiISR(args.pinin, wiringpi.INT_EDGE_RISING, isr)

dest_address = (args.host, args.port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    time.sleep(100)
sock.close()

