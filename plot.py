#!/usr/bin/env python2

import os
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 0), (0, 1, 1)]

path = "/home/andreas/Desktop/data"
files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".txt")]
print files

for i, path in enumerate(files):
    with open(path, "r") as f:
        data = [map(float, line.split()) for line in f.readlines()[:-1]]
    data = np.array(data)
    x, y = zip(*data)

    """
    coefs = poly.polyfit(x, y, 1)
    fit = poly.Polynomial(coefs)
    y0 = fit(x[0])
    x = x - x[0]
    y = y - y0 - x

    coefs = poly.polyfit(x, y, 1)
    fit = poly.Polynomial(coefs)
    """
    c = np.array(colors[i])

    plt.scatter(x, y, s=20, c=c, alpha=0.5, lw=0, label=os.path.basename(path))
    #plt.plot(x, fit(x), linewidth=1, color=c*0.5)

plt.legend()
plt.show()
