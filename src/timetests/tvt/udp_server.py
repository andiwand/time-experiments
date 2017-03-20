#!/usr/bin/env python2
# TODO: python3

import os
import argparse
import socket

from timetests import shared

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=str, help="data path")
parser.add_argument("-p", "--port", type=int, help="set port number (default %(default)d)", default=12345)
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", args.port))

clients = {}

try:
    while True:
        data, addr = sock.recvfrom(1024)
        t = shared.utc_nano()
        if addr[0] not in clients:
            print "%s:%d connected" % addr
            path = os.path.join(args.directory, addr[0].replace(".", "_") + ".txt")
            f = open(path, "a")
            clients[addr[0]] = {"log_path": path, "log_file": f}
        f = clients[addr[0]]["log_file"]
        f.write("%.9f %s\n" % (t, data))
        f.flush()
finally:
    sock.close()
    for addr in clients:
        f = clients[addr]["log_file"]
        f.close()
