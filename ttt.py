#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timezone

TRACKING_FILE = os.path.expanduser("~/.tracking")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1]
    if cmd == "+":
        start_tracking(sys.argv[2])
    elif cmd == "-":
        stop_tracking(sys.argv[2])
    elif cmd == "=":
        show_tracked()
    else:
        show_help()


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
