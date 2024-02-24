#!/usr/bin/env python3
from datetime import datetime, timedelta
from subprocess import call
import re, sys

CHRONICLES = "../../personal/lists/chronicles.txt"
MARKER = re.compile(">>>>>>>>>>>>>>>>>>>>>>>>>*")
COMPLETED = re.compile("[ \t]")

def formatDay(date):
    return "= " + date.strftime("%b %d | %a") + " =" + "=" * 16 + " " + str(date.year)

def generate_day_list():
    num_years = 20
    current_date = datetime.today()
    for _ in range(num_years * 365):
        print(formatDay(current_date))
        current_date += timedelta(days=1)

# generate_day_list() # save generated days to CHRONICLES

def data():
    f = open(CHRONICLES, "r")
    lines = f.readlines()
    return [l.rstrip() for l in lines]


#       way/
# find the current marker ">>>>>>>>>>>>>>>>>>>>>>>>>>>"
# and open vim to that the day before that line
def openChronicles():
    lines = data()
    n = 0
    for (i,l) in enumerate(lines):
        if l[0] == '=':
            n = i + 1
        if re.fullmatch(MARKER, l):
            call(["vim", "+"+str(n), CHRONICLES])
            return
    call(["vim", CHRONICLES])


def showOpen():
    lines = data()
    seen = []
    for l in lines:
        if len(l) == 0:
            continue
        if l[0] == ' ' or l[0] == '\t':
            continue;
        if l[0] == 'x' or l[0] == 'X' or l[0] == '=':
            if len(l) > 2 and l[1] == ' ':
                continue;
        if l in seen:
            continue
        seen.append(l)
        print(l)

def main():
    if len(sys.argv) == 1:
        showOpen()
        return
    if sys.argv[1] == "-e" or sys.argv[1] == "e":
        openChronicles()

if __name__ == "__main__":
    main()

