#!/usr/bin/env python3

import os
import argparse
import decimal

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="input file")
parser.add_argument("outfile", help="output file")
args = parser.parse_args()

with open(args.infile, "r") as f:
    pairs = [map(decimal.Decimal, line.split(" ")) for line in f.readlines()[:-1]]

with open(args.outfile, "w") as f:
    for pair in pairs:
        if str(pair[1]).split(".")[1].startswith("0000"):
            print(pair[1])
            continue
        f.write("%s %s\n" % tuple(map(str, pair)))
