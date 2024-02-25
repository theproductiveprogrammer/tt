#!/usr/bin/env python3
from datetime import datetime, timedelta
from subprocess import call
from datetime import datetime
import re, sys, os

import gcal

CHRONICLES = os.path.expanduser("~/Desktop/chaRcoal/personal/lists/chronicles.txt")
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

    def toISO(self):
        return f"{self.year}-{self.month:02}-{self.day:02}"

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
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)

    def toISOstart(self):
        return f"{self.dt.toISO()}T{self.start_h}:{self.start_m}:00"

    def toISOend(self):
        return f"{self.dt.toISO()}T{self.end_h}:{self.end_m}:00"

    def __str__(self):
        return f"Tm({self.dt}: {self.txt} @{self.start_h}:{self.start_m}-{self.end_h}:{self.end_m}-{self.notes})"

class Day:
    def __init__(self, dt, line):
        self.dt = dt
        self.line = line
        self.items = []

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
# go to the chronicles directory (for vim to work well)
# load the chronicles data then find the current
# current marker ">>>>>>>>>>>>>>>>>>>>>>>>>>>"
# and open vim to that the day before that line
def openChronicles():
    os.chdir(os.path.dirname(CHRONICLES))
    lines = data()
    n = 0
    for (i,l) in enumerate(lines):
        if not l:
            continue
        if l[0] == '=':
            n = i + 1
        if re.fullmatch(MARKER, l):
            call(["vim", "+"+str(n), CHRONICLES])
            return
    call(["vim", CHRONICLES])


#       understand/
# "open" lines are those that are not marked as done (.)
# or dropped (#)
#   . done line starts with a dot
#   # dropped line is discarded or moved to another day
#
#       way/
# We collect all open lines, discarding duplicates, and
# removing any days with no scheduled tasks
def getOpen():
    lines = data()
    open_ = []
    for l in lines:

        if not l:
            continue

        if l[0] == '.' or l[0] == '#':
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

#       way/
# gather open lines, ignore notes, sort the rest by day
# then show them
def showOpen():
    lines = getOpen()
    byday = gatherByDay(lines)
    for day in byday:
        print(day.line, flush=True)
        items = sortedItems(day)
        for item in items:
            if not isNote(item):
                print(item, flush=True)

def gatherByDay(lines):
    ret = []
    curr = None
    for l in lines:
        dt = xDt(l)
        if dt:
            curr = Day(dt, l)
            ret.append(curr)
        else:
            curr.items.append(l)
    return ret

#       way/
# sort the scheduled items first by time
# then the add rest
def sortedItems(day):
    sched = []
    rest = []
    for item in day.items:
        tm = xTm(day.dt, item)
        if tm:
            sched.append(item)
        else:
            rest.append(item)
    sched.sort(key = lambda l: xTm(day.dt, l).toISOstart())
    return sched + rest

#       way/
# filter all open items that are scheduled for today
def addToCalendar():
    scheduled = getTodaysSchedule()
    if not scheduled:
        print("Nothing scheduled today...")
        return
    for s in scheduled:
        gcal.addToGoogleCalendar(s)

def openCalendar():
    call(["open", "-a", "Safari.app", "https://calendar.google.com/calendar/u/5/r"])

def getTodaysSchedule():
    lines = getOpen()
    scheduled_today = []
    prev_dt = None
    currTm = None
    for l in lines:
        dt = xDt(l)
        if dt:
            prev_dt = dt
        tm = xTm(prev_dt, l)
        if tm and isToday(prev_dt):
            scheduled_today.append(tm)
            currTm = tm
        elif currTm and isNote(l):
            currTm.addNote(l)
        else:
            currTm = None
    return scheduled_today

def isToday(dt):
    today = datetime.now()
    return today.year == dt.year and today.month == dt.month and today.day == dt.day

def isNote(l):
    return l[0] == ' ' or l[0] == '\t'

def main():

    if len(sys.argv) == 1:
        openChronicles()
        return

    if sys.argv[1] == "-e" or sys.argv[1] == "e" or sys.argv[1] == "--edit" or sys.argv[1] == "edit":
        openChronicles()
        return

    if sys.argv[1] == "-s" or sys.argv[1] == "s" or sys.argv[1] == "--show" or sys.argv[1] == "show":
        showOpen()
        return

    if sys.argv[1] == "-c" or sys.argv[1] == "c" or sys.argv[1] == "--cal" or sys.argv[1] == "cal":
        addToCalendar()
        openCalendar()
        return

    print(f"Did not understand command line argument: '{sys.argv[1]}'")

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
        pass

