#!/usr/bin/env python3

import sys
import os

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


def show_help():
    print("ttt.py - Track time")
    print("Usage:")
    print("  ttt.py + <what>        # start tracking time against <what>")
    print("  ttt.py - <what>        # stop tracking time against <what>")
    print("  ttt.py =               # show times")

main()
