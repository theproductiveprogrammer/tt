#!/usr/bin/env python3
import sys
import os
import re
from datetime import datetime, timezone

TODO_FILE = os.path.expanduser("~/.ttdata")

#       understand/
# main entry point into our program
#       way/
# load the todo file and perform whatever
# operation the user has requested
def main():
    todos = load_todo()
    grant_user_request(todos)

def load_todo():
    try:
        with open(TODO_FILE) as f:
            return parse(f)
    except FileNotFoundError:
        return []

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
            for i in reversed(range(len(todos))):
                if todos[i].id == todo.id:
                    todos[i].updated = True
                    break
            todos.append(todo)
    num = 1
    for todo in reversed(todos):
        if not todo.updated:
            todo.ref = num
            num += 1
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
    request = " ".join(sys.argv[1:])
    resp = grant_request(request, todos)

    if not request:
        show(resp)
        return

    if request[0] == "=":
        show(resp)
        return

    if request[0] == "+":
        show(resp)
        update_file(todos)
        return

    if request[0] == '.':
        show(resp[0])
        show(resp[1])
        update_file(todos)
        return
    if request[0] == '^':
        show(resp[0])
        show(resp[1])
        update_file(todos)
        return

    if request[0] == 'n':
        show(resp)
        update_file(todos)
        return

def grant_request(request, todos):

    if not request:
        return showable(todos)

    if request[0] == "=":
        return get_filtered(todos, request[1:])

    if request[0] == "+":
        return add_new_todo(request[1:], todos)

    if request[0] == '.':
        return update(request, todos)

    if request[0] == '^':
        return update(request[1:], todos)

    if request[0] == 'n':
        return add_note(request[1:], todos)

    raise TTError("Did not understand " + request)


def update_file(todos):
    with open(TODO_FILE, 'a') as f:
        for todo in todos:
            if todo.dirty:
                f.write(save_format(todo) + "\n")


def add_note(request, todos):
    num, note = get_ref(request)
    if num == 0:
        raise TTError("Could not find reference for note")
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo_.notes.append(note)
            todo_.dirty = True
            return todo_


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
    elif request[0] == '^':
        return get_numbered_ref(request[1:])
    else:
        return get_numbered_ref(request)

def update(request, todos):
    num, request = get_ref(request)
    return update_todo(num, request, todos)

def update_todo(num, txt, todos):
    todo = make_new_todo(txt, todos)
    repl = None
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo.id = todo_.id
            todo.notes = todo_.notes
            todo_.updated = True
            if not todo.txt and not todo.tags:
                todo.txt = todo_.txt
                todo.tags = todo_.tags
            repl = todo_
            break
    append_todo(todo, todos)
    repl.ref = num
    return todo,repl

def add_new_todo(txt, todos):
    todo = make_new_todo(txt, todos)
    append_todo(todo, todos)
    return todo

def append_todo(todo, todos):
    for todo_ in todos:
        if todo_.ref:
            todo_.ref += 1
    todos.append(todo)

def make_new_todo(txt, todos):
    id = 1
    for todo in todos:
        if todo.id >= id:
            id = todo.id + 1
    todo = make_todo(False, id, datetime.now(timezone.utc), txt)
    todo.dirty = True
    todo.ref = 1
    return todo

def make_todo(closed, id, date, txt):
    todo = ToDo()
    txt = txt.strip()
    if txt:
        (todo.txt, todo.tags) = extract_tags(txt)
    todo.id = id
    todo.closed = closed
    todo.date = date
    return todo


def extract_tags(txt):
    tags = []
    p = re.compile("\s:([^\s:]*)|^:([^\s:]*)")
    m = p.search(txt)
    while m:
        txt = (txt[0:m.span()[0]].strip() + " " + txt[m.span()[1]:].strip()).strip()
        if m.group(1):
            tags.append(m.group(1))
        if m.group(2):
            tags.append(m.group(2))
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

        self.updated = False
        self.closed = False
        self.dirty = False

    def __repr__(self):
        closed = "x" if self.closed else "-"
        tags = ':'.join(self.tags)
        notes = '|'.join(self.notes)
        dirty = '*' if self.dirty else ""
        updated = 'XX' if self.updated else ""
        return f"ToDo<{updated}{closed}{self.id} {self.txt} :{tags}: #{self.ref} |{notes}| {dirty}{updated}>"


class TTError(Exception):
    pass


def save_format(todo):
    closed = "x" if todo.closed else "-"
    date = datetime.isoformat(todo.date)
    tags = " ".join([f":{t}" for t in todo.tags])
    notes = "\n".join(todo.notes)
    r = f"{closed} {todo.id}@{date}"
    if todo.txt:
        r = r + " " + todo.txt
    if tags:
        r = r + " " + tags
    if notes:
        r = r + "\n" + notes
    return r

def display_format(todo):
    if todo.ref < 5:
        ref = "." * todo.ref
    else:
        ref = todo.ref
    ref = f"{ref: <4}"
    closed = "x" if todo.closed else "-"
    tags = " ".join([f":{t}" for t in todo.tags])
    notes = "\n".join(todo.notes)
    r = f"{ref} {closed}"
    if todo.txt:
        r = r + " " + todo.txt
    if tags:
        r = r + " " + tags
    if notes:
        r = r + "\n" + notes
    return r

def show(todos):
    if not todos:
        print("")
        return
    if isinstance(todos, ToDo):
        todos = [todos]
    for todo in todos:
        print(display_format(todo))

def showable(todos):
    return [todo for todo in todos if not todo.updated and not todo.closed]

def get_filtered(todos, s):
    words = s.strip().split(" ")
    words = [w.lower() for w in words]
    return [todo for todo in todos if matches_1(words, todo)]

def matches_1(words, todo):
    for word in words:
        if todo.txt and word in todo.txt.lower():
            return True
        if todo.tags:
            for tag in todo.tags:
                if word in f":{tag.lower()}":
                    return True
    return False


if __name__ == "__main__":
    main()
