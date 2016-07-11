#!/usr/bin/env python2

import time
import argparse
import socket
import shared

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="host to connect")
parser.add_argument("-p", "--port", type=int, help="set port number (default 12345)",
                    default=12345)
parser.add_argument("-i", "--interval", type=int, help="set interval (default 1)",
                    default=1)
args = parser.parse_args()

socket_address = (args.host, args.port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        t = "%.9f" % shared.utc_nano()
        sock.sendto(t, socket_address)
        print t
        time.sleep(args.interval)
finally:
    sock.close()
