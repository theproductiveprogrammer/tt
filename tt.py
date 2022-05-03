#!/usr/bin/env python3
import sys
import os
import re
from datetime import datetime, timezone

#       understand/
# main entry point into our program
#       way/
# load the todo file and perform whatever
# operation the user has requested
def main():
    todos = load_todo()
    grant_user_request(todos)

def load_todo():
    TODO_FILE = os.path.expanduser("~/.ttdata")
    with open(TODO_FILE) as f:
        return parse(f)

#       way/
# for each line in the file, parse it as a
# todo, blitzing the previous todo (if any)
# it is updating (and copying it's notes across)
# or adding the line as a note to the current
# todo
#       understand/
# The todo file format:
# - [id] text :tag :tag :tag
# notes
# notes
# x [id] text :tag :tag :tag
def parse(lines):
    todos = []
    for line in lines:
        todo = parse_line(line)
        if todo is None:
            todo = todos[-1] if todos else ToDo()
            todo.notes.append(line.strip())
        else:
            todos.append(todo)
    return todos

def parse_line(line):
    if not line:
        return None
    p = re.compile("^([-x]) ([0-9]+)@(\d\d\d\d-[0-1]\d-[0-3]\dT[0-2]\d:[0-6]\d:[0-6]\d[0-9.+:]*) (.*)")
    m = p.search(line)
    if not m:
        return None
    closed = True if m.group(1) == "x" or m.group(1) == "X" else False
    id = int(m.group(2))
    date = datetime.fromisoformat(m.group(3))
    text = m.group(4)
    return make_todo(closed, id, date, text)


def grant_user_request(todos):
    print(todos)

def grant_request(request, todos):
    if not request:
        raise TTError("Nothing to do!")

    if request[0] == "+":
        add_new_todo(request[1:], todos)
    elif request[0] == '.':
        update(request, todos)
    elif request[0] == '^':
        update(request[1:], todos)
    elif request[0] == 'n':
        add_note(request[1:], todos)
    else:
        raise TTError("Did not understand " + request)


def add_note(request, todos):
    num, note = get_dotted_ref(request)
    if num == 0:
        raise TTError("Could not find reference for note")
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo_.notes.append(note)
            return


#       understand/
# we can reference todos using a "dotted notation":
#   .  < first/most recent todo
#   .. < second todo
#   ... < third todo
#   .... and so on
def get_dotted_ref(request):
    num = 0
    while request[0] == '.':
        num += 1
        request = request[1:]
    return num, request.strip()

def get_numbered_ref(request):
    p = re.compile("^[0-9]+")
    m = p.search(request)
    if not m:
        raise TTError("Could not find reference number")
    request = request[m.span()[1]:].strip()
    num = int(m.group(0))
    return (num, request)

def get_ref(request):
    if request[0] == '.':
        return get_dotted_ref(request)
    else:
        return get_numbered_ref(request)

def update(request, todos):
    num, request = get_ref(request)
    update_todo(num, request, todos)

def update_todo(num, txt, todos):
    todo = make_new_todo(txt, todos)
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo.id = todo_.id
            todo.notes = todo_.notes
    append_todo(todo, todos)

def add_new_todo(txt, todos):
    append_todo(make_new_todo(txt, todos), todos)

def append_todo(todo, todos):
    for todo_ in todos:
        todo_.ref += 1
    todos.append(todo)

def make_new_todo(txt, todos):
    id = 1
    for todo in todos:
        if todo.id >= id:
            id += 1
    todo = make_todo(False, id, datetime.now(timezone.utc), txt)
    todo.dirty = True
    todo.ref = 1
    return todo

def make_todo(closed, id, date, txt):
    todo = ToDo()
    txt = txt.strip()
    if not txt:
        raise TTError("Todo item empty")
    (todo.txt, todo.tags) = extract_tags(txt)
    todo.id = id
    todo.closed = closed
    todo.date = date
    return todo


def extract_tags(txt):
    tags = []
    p = re.compile(":([^\s:]*)")
    m = p.search(txt)
    while m:
        txt = (txt[0:m.span()[0]].strip() + " " + txt[m.span()[1]:]).strip()
        if m.group(1):
            tags.append(m.group(1))
        m = p.search(txt)
    return (txt, tags)

def get_todo_item(todos, num):
    for todo in reversed(todos):
        if todo.ref == num:
            return todo

class ToDo:
    def __init__(self):
        self.id = None
        self.ref = None
        self.txt = None
        self.tags = []
        self.notes = []
        self.date = None

        self.closed = False
        self.dirty = False

    def __repr__(self):
        return f"ToDo<{self.id} {self.txt} :{':'.join(self.tags)}: #{self.ref} |{'|'.join(self.notes)}| {'*' if self.dirty else None}>"


class TTError(Exception):
    pass

if __name__ == "__main__":
    main()
