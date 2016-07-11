#!/usr/bin/env python2

import os
import argparse
import socket
import shared

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=str, help="data path")
parser.add_argument("-p", "--port", type=int, help="set port number (default 12345)",
                    default=12345)
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", args.port))

clients = {}

try:
    while True:
        data, addr = sock.recvfrom(1024)
        t = "%.9f" % shared.utc_nano()
        if addr not in clients:
            print "%s:%d connected" % addr
            path = os.path.join(args.directory, addr[0].replace(".", "_") + ".txt")
            f = open(path, "a")
            clients[addr] = {"log_path": path, "log_file": f}
        f = clients[addr]["log_file"]
        f.write(t)
        f.write(" ")
        f.write(data)
        f.write("\n")
finally:
    sock.close()
    for addr in clients:
        f = clients[addr]["log_file"]
        f.close()
