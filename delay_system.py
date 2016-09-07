#!/usr/bin/env python3

import time
import argparse
import shared

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interval", type=float, help="set interval (default 1)",
                    default=1)
args = parser.parse_args()

while True:
    t = -shared.time() + shared.time()
    time.sleep(args.interval)
    print(t)

