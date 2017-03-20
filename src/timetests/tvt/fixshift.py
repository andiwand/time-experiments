#!/usr/bin/env python3

path = "/home/andreas/Desktop/data/192_168_15_130.txt"

with open(path, "r") as f:
    data = [map(float, line.split()) for line in f.readlines()]

with open(path + ".shift", "w") as f:
    for d in data:
        f.write("%.9f" % d[0])
        f.write(" ")
        f.write("%.9f" % (d[1] - 3600*2))
        f.write("\n")

