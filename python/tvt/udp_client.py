#!/usr/bin/env python3

import time
import argparse
import socket
import shared

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="host to connect")
parser.add_argument("-p", "--port", type=int, help="set port number (default %(default)d)",
                    default=12345)
parser.add_argument("-i", "--interval", type=float, help="set interval (default %(default)d)",
                    default=1)
args = parser.parse_args()

socket_address = (args.host, args.port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        t = "%.9f" % shared.utc_nano()
        sock.sendto(t.encode(), socket_address)
        print(t)
        time.sleep(args.interval)
finally:
    sock.close()

