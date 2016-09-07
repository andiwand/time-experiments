#!/usr/bin/env python3

import time
import argparse
import wiringpi
import shared

time_start = 0
time_end = 0

def isr():
    global time_end
    time_end = shared.time()
    return True

parser = argparse.ArgumentParser()
parser.add_argument("pinin", type=int, help="input pin")
parser.add_argument("pinout", type=int, help="output pin")
parser.add_argument("-i", "--interval", type=float, help="set interval (default 1)",
                    default=1)
args = parser.parse_args()

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(args.pinout, 1) # output
wiringpi.pinMode(args.pinin, 0) # input
wiringpi.pullUpDnControl(args.pinin, 1) # pull up
wiringpi.wiringPiISR(args.pinin, wiringpi.INT_EDGE_RISING, isr)

while True:
    time_end = 0
    wiringpi.digitalWrite(args.pinout, 1)
    time_start = shared.time()
    wiringpi.digitalWrite(args.pinout, 0)
    time.sleep(args.interval)
    t = time_end - time_start
    print(t)

