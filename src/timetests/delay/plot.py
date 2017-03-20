#!/usr/bin/env python3

import os
import argparse
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="path to data")
parser.add_argument("-b", "--bins", type=int, help="number of bins", default=50)
args = parser.parse_args()

with open(args.path, "r") as f:
    data = [float(line) for line in f.readlines()]
data = np.array(data)
mu, sigma = np.mean(data), np.std(data)
print(str(mu) + " +/- " + str(sigma))

n, bins, patches = plt.hist(data, args.bins, normed=1, facecolor="g")
plt.plot(bins, mlab.normpdf(bins, mu, sigma), "r--", linewidth=1)

plt.show()

