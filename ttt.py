#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timezone
from subprocess import call

EDITOR = os.environ.get('EDITOR', 'vim')

TRACKING_FILE = os.path.expanduser("~/.tttracking")
TRACKING_LATEST_FILE = os.path.expanduser("~/.tttracking.latest")
COMPLETION_FILE = os.path.expanduser("~/.tttracking.completions")

WORK_CYCLES_FILE = os.path.expanduser("~/.work-cycles")
WORK_CYCLES_LATEST_FILE = os.path.expanduser("~/.work-cycles.latest")

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
        last_what = None
        last_dt = None
        with open(TRACKING_FILE) as f:
            for l in f:
                if l.startswith("#"):
                    if last_what:
                        val = (l[0], (l[1:], last_dt))
                        v = recs.get(last_what)
                        v.append(val)
                    continue;
                [dt,what] = l[1:].split("\t")
                what = what.strip()
                v = recs.get(what)
                if not v:
                    v = []
                    recs[what] = v
                dt = datetime.fromisoformat(dt)
                val = (l[0], dt)
                v.append(val)
                last_what = what
                last_dt = dt


    except FileNotFoundError:
        pass

    return recs

def show_daily_tracked(recs):
    daily_recs = {}
    dt = None
    for what,vals in recs.items():
        for val in vals:
            if val[0] == '+':
                dt = val[1].strftime('%Y-%m-%d %a')
            d = daily_recs.get(dt)
            if not d:
                d = {}
                daily_recs[dt] = d
            v = d.get(what)
            if not v:
                v = []
                d[what] = v
            v.append(val)
    toShow = []
    for k,v in daily_recs.items():
        inserted = False
        i = 0
        while not inserted and i < len(toShow):
            (k_,v_) = toShow[i]
            if k_ > k:
                inserted = True
                toShow.insert(i,(k,v))
            i += 1;
        if not inserted:
            toShow.append((k,v))
    for k,v in toShow:
        print('\n\n')
        print('\t\t\t\t'+k)
        tot = show_tracked(v)
        print("["+fmtTm(tot)+"]")

def show_tracked(recs):
    now_ = datetime.now().astimezone()
    tot_ = now_ - now_
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
        tot = now_ - now_
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
            elif t == '-':
                tm =  dt - prev
                tot = tot + tm
                tot_ = tot_ + tm
                print(" [" + fmtTm(tm) + "]")

        if last == "+":
            print()

        tot = str(tot)
        ndx = tot.rfind(".")
        if ndx != -1:
            tot = tot[:ndx]
        print("= " + str(tot))

        print()
    return tot_


def fmtTm(tm):
    tm = str(tm)
    ndx = tm.rfind(".")
    if ndx != -1:
        tm = tm[:ndx]
    return tm



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
    close_ultraworking(what, now);
    with open(TRACKING_FILE, 'a') as f:
        rec_ = "-" + now + "\t" + what
        f.write(rec_ + "\n")
        v = ('-', now_)
        rec.append(v)
        print("stopped: " + what + " [" + tm + "] ###")

def start_tracking(recs, what):
    now = datetime.isoformat(datetime.now().astimezone())
    open_new_ultraworking(what, now);
    with open(TRACKING_FILE, 'a') as f:
        rec = "+" + now + "\t" + what
        f.write(rec + "\n")
        print("started: " + what)

def open_new_ultraworking(what, now):
    template = f"""
------------------------------------------------
                {now}
# {what}

Q. What am I trying to accomplish this cycle?
A. 


Q. How will I get started?
A. 


Q. Any hazards present?
A. 


Energy: L|M|H
Morale: L|M|H

    """.strip()

    with open(WORK_CYCLES_LATEST_FILE, 'w') as f:
        f.write(template)
    call([EDITOR,"+exe '/A' | norm $","+startinsert!",WORK_CYCLES_LATEST_FILE])

def close_ultraworking(what, now):
    template = f"""
.                         REVIEW      ----------
                {now}
Q. Completed target?
A. Y|1/2|N


Q. Anything noteworthy?
A. 


Q. Any distractions?
A. 


Q. Things to improve for the next cycle?
A. 
    """.strip()

    template = ' ' + template[1:]
    template = template + " \n\n\n\n"

    with open(WORK_CYCLES_LATEST_FILE, 'r') as f:
        txt = f.read()
        txt = txt + "\n" + template
        with open(WORK_CYCLES_FILE, 'a') as f:
            f.write(txt)
    call([EDITOR,"+exec 'norm G' | exec '?Completed' | norm jA",WORK_CYCLES_FILE])



def record_latest(what):
    with open(TRACKING_LATEST_FILE, 'w') as f:
        f.write(what)

def remove_latest():
    f = open(TRACKING_LATEST_FILE, "w")
    f.truncate(0)
    f.close()

def record_completions(recs, what):
    with open(COMPLETION_FILE, 'w') as f:
        for k in recs.keys():
            f.write(k + "\n")
        f.write(what)


def edit_data():
    call([EDITOR,TRACKING_FILE])

def show_help():
    print("ttt.py - Track time")
    print("Usage:")
    print("  ttt.py [+] <what>        # start tracking time against <what>")
    print("  ttt.py - <what>        # stop tracking time against <what>")
    print("  ttt.py =               # show times")

main()
