#!/usr/bin/env python

import os
import time
import socket

SOL_NETLINK = 270
NETLINK_ADD_MEMBERSHIP = 1

MY_GROUP = 31

sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, socket.NETLINK_USERSOCK)

sock.bind((os.getpid(), MY_GROUP))
sock.setsockopt(SOL_NETLINK, NETLINK_ADD_MEMBERSHIP, MY_GROUP)

while True: print sock.recv(65535)

