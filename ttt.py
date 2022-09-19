#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timezone

TRACKING_FILE = os.path.expanduser("~/.tracking")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    recs = load()

    cmd = sys.argv[1]
    if cmd == "+":
        start_tracking(recs, sys.argv[2])
    elif cmd == "-":
        stop_tracking(recs, sys.argv[2])
    elif cmd == "=":
        show_tracked(recs)
    else:
        show_help()

def load():
    recs = {}
    try:

        with open(TRACKING_FILE) as f:
            for l in f:
                [dt,what] = l[1:].split("\t")
                what = what.strip()
                v = recs.get(what)
                if not v:
                    v = []
                    recs[what] = v
                val = (l[0], datetime.fromisoformat(dt))
                v.append(val)


    except FileNotFoundError:
        pass

    return recs

def show_tracked(recs):
    for what,vals in recs.items():
        print("### " + what + " ###")
        prev = None
        tot = None
        last = "+"
        for v in vals:
            (t,dt) = v
            last = t
            if t == "+":
                dts = datetime.isoformat(dt)
                ndx = dts.rfind(".")
                if ndx != -1:
                    dts = dts[:ndx]
                dts = dts.replace("T", " ")
                print(dts, end=" ")
                prev = dt
            else:
                tm =  dt - prev
                if tot:
                    tot = tot + tm
                else:
                    tot = tm
                tm = str(tm)
                ndx = tm.rfind(".")
                if ndx != -1:
                    tm = tm[:ndx]
                print(" [" + tm + "]")

        if last == "+":
            print()

        tot = str(tot)
        ndx = tot.rfind(".")
        if ndx != -1:
            tot = tot[:ndx]
        print("= " + str(tot))

        print()


def stop_tracking(recs, what):
    rec = recs.get(what)
    if not rec or not rec[-1]:
        print(what + " not started")

    (t,dt) = rec[-1]
    tm = datetime.now(timezone.utc) - dt
    tm = str(tm)
    ndx = tm.rfind(".")
    if ndx != -1:
        tm = tm[:ndx]

    if t == "-":
        print(what + " already stopped - " + tm)
        return

    now = datetime.isoformat(datetime.now(timezone.utc))
    with open(TRACKING_FILE, 'a') as f:
        rec = "-" + now + "\t" + what
        f.write(rec + "\n")
        print("stopped: " + what + " [" + tm + "]")

def start_tracking(recs, what):
    rec = recs.get(what)

    if rec and rec[-1]:
        (t,dt) = rec[-1]
        if t == "+":
            tm = datetime.now(timezone.utc) - dt
            tm = str(tm)
            ndx = tm.rfind(".")
            if ndx != -1:
                tm = tm[:ndx]
            print(what + " already being tracked - " + tm)
            return

    now = datetime.isoformat(datetime.now(timezone.utc))
    with open(TRACKING_FILE, 'a') as f:
        rec = "+" + now + "\t" + what
        f.write(rec + "\n")
        print("started: " + what)

def show_help():
    print("ttt.py - Track time")
    print("Usage:")
    print("  ttt.py + <what>        # start tracking time against <what>")
    print("  ttt.py - <what>        # stop tracking time against <what>")
    print("  ttt.py =               # show times")

main()
