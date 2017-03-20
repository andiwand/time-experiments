#!/usr/bin/env python3

import time
import argparse

from timetests import shared

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="host to connect")
parser.add_argument("-i", "--interval", type=float, help="set interval (default 1)",
                    default=1)
args = parser.parse_args()

while True:
    t = shared.ping(args.host)
    print(t)
    time.sleep(args.interval)

