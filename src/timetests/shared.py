import sys
import time as pytime
import datetime
import shlex
import subprocess
import numpy as np

if hasattr(pytime, "perf_counter"):
    perftime = pytime.perf_counter
elif sys.platform == "win32":
    perftime = pytime.clock
else:
    perftime = pytime.time

if sys.platform == "win32":
    time = pytime.clock
else:
    time = pytime.time

def utc_nano():
    utc = pytime.mktime(datetime.datetime.utcnow().timetuple())
    t = time()
    if int(utc % 100) - int(t % 100) > 50:
        t = int(utc / 100) * 100 + t % 100 + 100
    elif int(t % 100) > int(utc % 100):
        t = int(utc / 100) * 100 + t % 100
    else:
        t = utc + t - int(t)
    return t

def ping(dest, timeout=5):
    import ping as pingimpl
    return pingimpl.do_one(dest, timeout)

def call(cmd):
    return subprocess.call(shlex.split(cmd))

def call_bool(cmd):
    return True if call(cmd) == 0 else False

def reject_outliers_std(data, m=2):
    # https://stackoverflow.com/a/11686764
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def reject_outliers_median(data, m=2):
    # https://stackoverflow.com/a/16562028
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]

def reject_outliers_iqr(data, iq_range=0.5):
    # https://stackoverflow.com/a/39424972
    pcnt = (1 - iq_range) / 2.0 * 100
    qlow, median, qhigh = np.percentile(data, [pcnt, 50, 100 - pcnt])
    iqr = qhigh - qlow
    return data[np.absolute(data - median) <= iqr]
