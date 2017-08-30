#!/usr/bin/env python3

import os
import math
import decimal
import argparse
import threading
import subprocess

def run_pps_pulse(args):
    global debug, pps_time
    with subprocess.Popen([args.pps_pulse, args.pps_device], stdout=subprocess.PIPE) as p:
        for line in p.stdout:
            line = line.decode("us-ascii")
            pps_time = decimal.Decimal(line)
            if debug: print("pps", pps_time)

def run_nmea_pulse(args):
    global debug, last_time
    

parser = argparse.ArgumentParser(description="measures the delay between pps and nmea pulse")
parser.add_argument("nmea_pulse", type=str, help="nmea_pulse path")
parser.add_argument("nmea_device", type=str, help="nmea device path")
parser.add_argument("pps_pulse", type=str, help="pps_pulse path")
parser.add_argument("pps_device", type=str, help="pps device path")
parser.add_argument("-d", "--debug", help="enable debugging", action="store_true")
parser.add_argument("-s", "--summery", help="show summery on exit", action="store_true")
args = parser.parse_args()

debug = args.debug
pps_time = None

t = threading.Thread(target=run_pps_pulse, args=(args,))
t.daemon = True
t.start()

sum1 = decimal.Decimal(0)
sum2 = decimal.Decimal(0)
count = 0

try:
    with subprocess.Popen([args.nmea_pulse, args.nmea_device], stdout=subprocess.PIPE) as p:
        for line in p.stdout:
            line = line.decode("us-ascii")
            nmea_time = decimal.Decimal(line)
            if debug: print("nmea", nmea_time)
            if not pps_time: continue
            diff = nmea_time - pps_time
            print(diff)
            if args.summery:
                sum1 += diff
                sum2 += diff**2
                count += 1
finally:
    if args.summery:
        print("")
        print("")
        print("summery:")
        print("count:", count)
        print("mean:", sum1 / count)
        print("std:", (sum2 / count - (sum1 / count) ** 2).sqrt())
