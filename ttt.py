#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timezone
from subprocess import call

TRACKING_FILE = os.path.expanduser("~/.tttracking")
LATEST_FILE = os.path.expanduser("~/.tttracking.latest")
COMPLETION_FILE = os.path.expanduser("~/.tttracking.completions")

def main():
    recs = load()

    if len(sys.argv) < 2:
        show_daily_tracked(recs)
        return

    cmd = sys.argv[1]
    val = ' '.join(sys.argv[2:])
    if cmd == "+":
        add(recs, val)
    elif cmd == "-":
        stop_tracking(recs)
        remove_latest()
    elif cmd == "=":
        show_tracked(recs)
    elif cmd == "-e":
        edit_data()
    elif cmd == "-h":
        show_help()
    else:
        val = ' '.join(sys.argv[1:])
        add(recs, val)

def add(recs, val):
    stop_tracking(recs)
    start_tracking(recs, val)
    record_latest(val)
    record_completions(recs, val)

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

def show_daily_tracked(recs):
    daily_recs = {}
    dt = None
    for what,vals in recs.items():
        for val in vals:
            if val[0] == '+':
                dt = val[1].strftime('%Y-%m-%d')
            d = daily_recs.get(dt)
            if not d:
                d = {}
                daily_recs[dt] = d
            v = d.get(what)
            if not v:
                v = []
                d[what] = v
            v.append(val)
    for k,v in daily_recs.items():
        print('\n\n')
        print('\t\t\t\t'+k)
        show_tracked(v)

def show_tracked(recs):
    toshow = []
    for what,vals in recs.items():
        inserted = False
        i = 0
        last = vals[-1][1]
        while not inserted and i < len(toshow):
            (w,v) = toshow[i]
            l = v[-1]
            if l[1] > last:
                inserted = True
                toshow.insert(i,(what,vals))
            i += 1
        if not inserted:
            toshow.append((what,vals))

    for what,vals in toshow:
        print("### " + what + " ###")
        prev = None
        tot = None
        last = "+"
        for v in vals:
            (t,dt) = v
            last = t
            if t == "+":
                dts = dt.astimezone().isoformat()
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


def stop_tracking(recs):
    for k in recs.keys():
        stop_tracking_(k, recs[k])

def stop_tracking_(what, rec):
    if not rec or not rec[-1]:
        return

    (t,dt) = rec[-1]
    if t == "-":
        return

    now_ = datetime.now().astimezone()
    tm = now_ - dt
    tm = str(tm)
    ndx = tm.rfind(".")
    if ndx != -1:
        tm = tm[:ndx]

    now = datetime.isoformat(now_)
    with open(TRACKING_FILE, 'a') as f:
        rec_ = "-" + now + "\t" + what
        f.write(rec_ + "\n")
        v = ('-', now_)
        rec.append(v)
        print("stopped: " + what + " [" + tm + "] ###")

def start_tracking(recs, what):
    rec = recs.get(what)

    if rec and rec[-1]:
        (t,dt) = rec[-1]
        if t == "+":
            tm = datetime.now().astimezone() - dt
            tm = str(tm)
            ndx = tm.rfind(".")
            if ndx != -1:
                tm = tm[:ndx]
            print(what + " already being tracked - " + tm)
            return

    now = datetime.isoformat(datetime.now().astimezone())
    with open(TRACKING_FILE, 'a') as f:
        rec = "+" + now + "\t" + what
        f.write(rec + "\n")
        print("started: " + what)

def record_latest(what):
    with open(LATEST_FILE, 'w') as f:
        f.write(what)

def remove_latest():
    f = open(LATEST_FILE, "w")
    f.truncate(0)
    f.close()

def record_completions(recs, what):
    with open(COMPLETION_FILE, 'w') as f:
        for k in recs.keys():
            f.write(k + "\n")
        f.write(what)


def edit_data():
    EDITOR = os.environ.get('EDITOR', 'vim')
    call([EDITOR,TRACKING_FILE])

def show_help():
    print("ttt.py - Track time")
    print("Usage:")
    print("  ttt.py [+] <what>        # start tracking time against <what>")
    print("  ttt.py - <what>        # stop tracking time against <what>")
    print("  ttt.py =               # show times")

main()
