import time
import datetime

def utc_nano():
    utc = time.mktime(datetime.datetime.utcnow().timetuple())
    t = time.time()
    if int(utc % 100) - int(t % 100) > 50:
        t = int(utc / 100) * 100 + t % 100 + 100
    elif int(t % 100) > int(utc % 100):
        t = int(utc / 100) * 100 + t % 100
    else:
        t = utc + t - int(t)
    return t
