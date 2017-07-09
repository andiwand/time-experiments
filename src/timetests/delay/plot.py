#!/usr/bin/env python3

import os
import argparse
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import shared

units = {'s': (1, r's'), 'ms': (1000, r'ms'), 'us': (1000000, r'\mu s')}

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='+', type=str, help='path to data')
parser.add_argument('-l', '--label', nargs='+', type=str, help='plot labels')
parser.add_argument('-b', '--bins', type=int, help='number of bins', default=50)
parser.add_argument('-u', '--unit', type=str, help='x unit (defaults to %(default)s)', default='s')
parser.add_argument('--zero', help='start at 0', action='store_true')
parser.add_argument('--no-fit', help='dont fit data with norm pdf', action='store_true')
parser.add_argument('--fit-points', type=int, help='point count for fitting line', default=500)
parser.add_argument('--outlier', type=float, help='outlier filter arg', default=6)
# TODO: option to plot min avg max
args = parser.parse_args()

factor, unit = units[args.unit]
data = []

for f in args.file:
    with open(f, 'r') as f:
        d = [float(line) for line in f.readlines()]
    d = np.array(d)
    d *= factor
    # TODO: store min max
    d = shared.reject_outliers_median(d, args.outlier)
    data.append(d)

label = args.label if args.label else args.file
n, bins, patches = plt.hist(data, args.bins, histtype='stepfilled', normed=True, edgecolor='black', linewidth=1, alpha=0.8, label=label)

start = 0 if args.zero else bins[0]

if not args.no_fit:
    print('label', 'mean', 'std')
    for d, p, l in zip(data, patches, label):
        mu, sigma = np.mean(d), np.std(d)
        print(l, mu, sigma)
        c = np.array(p[0].get_facecolor()) * 0.5
        c[3] = 1
        x = np.linspace(start, bins[-1], args.fit_points)
        y = mlab.normpdf(x, mu, sigma)
        plt.plot(x, y, lw=2, c=c, ls='--')

plt.gca().set_xlim([ start, bins[-1] ])

plt.xlabel('Delay [$%s$]' % unit)
plt.ylabel('Probability density')
plt.grid(True)
plt.legend()

plt.show()

