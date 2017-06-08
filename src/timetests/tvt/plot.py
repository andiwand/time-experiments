#!/usr/bin/env python2

# TODO: improve update; seek file to previous position; keep static plot options
# TODO: center option

import os
import argparse
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

colors = [(1, 0, 0), (0, 0, 1), (1, 0, 1), (1, 1, 0), (0, 1, 1), (0, 1, 0)]

def read(files, offsets=None):
    data = []
    for i, path in enumerate(files):
        offset = offsets[i] if offsets else 0
        with open(path, "r") as f:
            pairs = [map(float, line.split(" ")) for line in f.readlines()[:-1]]
        pairs = np.array(pairs)
        x, y = pairs[:,0], pairs[:,1]
        y = y - x
        x, y = x[offset:], y[offset:]
        single = {"x": x, "y": y}
        if args.group: single = group(single, args.group_time, args.min_group_size, args.dropout_max)
        if args.overlap: single = overlap(single)
        data.append(single)
    return data

def plot(data, names, colors):
    plots = []
    for i, name in enumerate(names):
        c = np.array(colors[i])
        x, y, std = map(data[i].get, ["x", "y", "std"])
        if std is not None:
            upper = y + std
            lower = y - std
            plt.fill_between(x, lower, upper, facecolor=c, alpha=0.3)
            plt.plot(x, y, c=c, lw=2, label=name)
        #plt.scatter(x, y, s=20, c=c, marker="o", alpha=0.5, lw=0, label=name)
        scatter, = plt.plot(x, y, marker="o", markerfacecolor=c, markeredgecolor=None, markeredgewidth=0, alpha=0.5, lw=0, label=name)
        plots.append({"scatter": scatter})
    return plots

def plot_update(data, plots):
    for i, single in enumerate(data):
        x, y, std = map(single.get, ["x", "y", "std"])
        scatter = plots[i]["scatter"]
        scatter.set_data(x, y)
    plt.draw()

def group(single, time, minsize, dropmax):
    result = {k: [] for k in ("x", "y", "std", "count")}
    i = 0
    x, y = single["x"], single["y"]
    while i < len(x):
        group_x = []
        time_end = x[i] + time
        while i < len(x) and x[i] < time_end:
            group_x.append(x[i])
            i += 1
        count = len(group_x)
        group_x = np.array(group_x)
        mean_x = np.mean(group_x)
        group_y = y[i-count:i].tolist()
        group_y.sort()
        group_y = np.array(group_y[dropmax:-dropmax-1])
        if len(group_x) < minsize:
            continue
        mean_y, std_y = np.mean(group_y), np.std(group_y)
        result["x"].append(mean_x)
        result["y"].append(mean_y)
        result["std"].append(std_y)
        result["count"].append(count)
    result = {k: np.array(result[k]) for k in result}
    return result

def overlap(single):
    pass

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="+", help="path to data file")
parser.add_argument("--overlap", help="overlap plots", action="store_true")
parser.add_argument("--group", help="group measurements", action="store_true")
parser.add_argument("--group-time", type=float, help="group data between given time", default=20)
parser.add_argument("--min-group-size", type=int, help="minimal size of the group", default=10)
parser.add_argument("--dropout-max", type=int, help="drop n maximum values of the group", default=3)
parser.add_argument("--update", help="live update data", action="store_true")
args = parser.parse_args()

data = read(args.file)
names = list(map(os.path.basename, args.file))
plots = plot(data, names, colors)

def handle_close(event):
    global run
    run = False
fig = plt.gcf()
fig.canvas.mpl_connect("close_event", handle_close)

plt.legend()

if not args.update:
    plt.show()
else:
    plt.ion()
    run = True
    while run:
        data = read(args.file)
        plot_update(data, plots)
        plt.pause(0.5)
