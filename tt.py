#!/usr/bin/env python3
from datetime import datetime, timedelta
from subprocess import call
from datetime import datetime
import re, sys, os

CHRONICLES = os.path.expanduser("~/chronicles.txt")
MARKER = re.compile(r">>>>>>>>>>>>>>>>>>>>>>>>>*")
COMPLETED = re.compile(r"[ \t]")
DATEFMT = re.compile(r"= ([A-Z][a-z][a-z]) ([0-3][0-9]) \| ([A-Z][a-z][a-z]) ======* ([0-9][0-9][0-9][0-9])")
SCHEDULED = re.compile(r"(.*) @([0-2][0-9]):([0-5][0-9])-([0-2][0-9]):([0-5][0-9])")

def formatDay(date):
    return "= " + date.strftime("%b %d | %a") + " =" + "=" * 16 + " " + str(date.year)

mnth = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
class Dt:
    def __init__(self, year, monthname, day, weekday):
        self.year = int(year)
        self.monthname = monthname
        self.month = mnth.index(monthname) + 1
        self.day = int(day)
        self.weekday = weekday

    def __str__(self):
        return f"Dt({self.year}-{self.monthname}-{self.day}[{self.weekday}])"

class Tm:
    def __init__(self, dt, txt, start_h, start_m, end_h, end_m):
        self.dt = dt
        self.txt = txt
        self.start_h = start_h
        self.start_m = start_m
        self.end_h = end_h
        self.end_m = end_m

    def __str__(self):
        return f"Tm({self.dt}: {self.txt} @{self.start_h}:{self.start_m}-{self.end_h}:{self.end_m})"

def xDt(l):
    if not l:
        return
    m = re.match(DATEFMT, l)
    if m:
        (m,d,w,y) = m.groups()
        return Dt(y, m, d, w)

def xTm(dt, l):
    if not l:
        return
    m = re.match(SCHEDULED, l)
    if m:
        (txt, start_h, start_m, end_h, end_m) = m.groups()
        return Tm(dt, txt, start_h, start_m, end_h, end_m)


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


def getOpen():
    lines = data()
    open_ = []
    for l in lines:

        if len(l) == 0:
            continue

        if l[0] == ' ' or l[0] == '\t':
            continue;

        if l[0] == 'x' or l[0] == 'X':
            if len(l) > 2 and l[1] == ' ':
                continue;

        if l in open_:
            continue

        open_.append(l)

    return removeEmptyDays(open_)

def removeEmptyDays(lines):
    lines.reverse()
    ret = []
    justSawADate = False
    for l in lines:
        if xDt(l):
            if justSawADate:
                continue
            justSawADate = True
        else:
            justSawADate = False
        ret.append(l)
    ret.reverse()
    return ret

def showOpen():
    lines = getOpen()
    for l in lines:
        print(l, flush=True)

#       way/
# filter all open items that are scheduled for today
def addToCalendar():
    scheduled = getTodaysSchedule()
    if not scheduled:
        print("Nothing scheduled today...")
        return
    for s in scheduled:
        print(f"Scheduling {s}")

def getTodaysSchedule():
    lines = getOpen()
    scheduled_today = []
    prev_dt = None
    for l in lines:
        dt = xDt(l)
        if dt:
            prev_dt = dt
        tm = xTm(prev_dt, l)
        if tm and isToday(prev_dt):
            scheduled_today.append(tm)
    return scheduled_today

def isToday(dt):
    today = datetime.now()
    return today.year == dt.year and today.month == dt.month and today.day == dt.day

def main():

    if len(sys.argv) == 1:
        openChronicles()
        return

    if sys.argv[1] == "-e" or sys.argv[1] == "e":
        openChronicles()
        return

    if sys.argv[1] == "-s" or sys.argv[1] == "s" or sys.argv[1] == "--show" or sys.argv[1] == "show":
        showOpen()
        return

    if sys.argv[1] == "-c" or sys.argv[1] == "c" or sys.argv[1] == "--cal" or sys.argv[1] == "cal":
        addToCalendar()
        return

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
        pass

