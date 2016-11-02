#!/usr/bin/env python3

import argparse
import shared

def ntp_start():
    return shared.call_bool("service ntp start")

def ntp_stop():
    return shared.call_bool("service ntp stop")

def ntp_restart():
    return shared.call_bool("service ntp restart")

def clock_set(dt):
    dt = dt.isoformat("  ")
    return shared.call_bool("date -s \"%s\"" % dt)

def clock_adjtimex(offset, freq):
    pass
