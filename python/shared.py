import sys
import time as pytime
import datetime

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

