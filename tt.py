#!/usr/bin/env python3

##** # tt (task tracker)
##**
##** A simple, yet powerful, task tracker
##**
##** ## Background
##**
##** Task tracking is a surprisingly complex and unwieldy beast. What works for one often does not satisfy his friend.
##** Sometimes the system cannot do something one person finds essential, while another is annoyed by the plethora of
##** features that just get in his way when he "just wants to get something simple done".
##**
##** Task Tracker, then - is not promising to be everything for everyone. Rather it is designed to serve me and get
##** _my_ tasks done smoothly and simply.
##**
##** ## How it works
##**
##** `tt` is a command-line utility that can quickly add new tasks and filter them by tag. By default it orders tasks
##** based on when they were added and when they are modified. Latest tasks are highest on the list. This, I find, gives
##** an excellent heuristic for _what is important_ mixed nicely with _what you need to do *now*_.
##**
##** Notes can be added to tasks which I find also are immensely useful. Tasks cannot be nested - I find that is more
##** convenient to use :tags to label tasks and sub tasks and filter them that way.
##**
##** ## Why it works
##**
##** It is amazingly fast to add, close, and review the entire task list. It stays out of my way and takes less than a
##** fraction of a second to perform any activity - from pulling up tasks, closing tasks, and adding new tasks. It is
##** cleverly designed to make it easier to manage tasks higher up in the list than lower and that also drives the
##** value it provides - prioritized tasks are just easier to work on than lower priority tasks. Finally, it uses a
##** simple text file to store everything, using a log datastore which makes it almost impossible to corrupt. All-in-all
##** an excellent solution for my own needs.


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
    todos = load_todos()
    grant_user_request(todos)

#       way/
# load todo's from a the TODO file
# and append daily tasks
def load_todos():
    todos = load_file_todos()
    return append_daily_tasks(todos)


def load_file_todos():
    try:
        with open(TODO_FILE) as f:
            return parse(f)
    except FileNotFoundError:
        return []


#       understand/
# daily tasks must be re-created every day
# so we look for daily tasks that have been
# closed earlier than a day and re-create them
def append_daily_tasks(todos):
    now = datetime.now()
    opened = []
    for option in todos:
        if option.updated or not option.closed:
            continue
        if "(daily)" in option.txt.lower():
            d = option.date.astimezone()
            if now.date() != d.date():
                todo = ToDo(option)
                todo.date = datetime.now(timezone.utc)
                todo.closed = False
                todo.dirty = True
                option.updated = True
                opened.append(todo)
    for todo in opened:
        append_todo(todo, todos)
        update_file(todo)
    return todos


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
        if not todo.updated and not todo.closed:
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

def show_help():
    print("""tt.py : todo list manager

By default shows list of things to do. Otherwise reponds to commands:

    -h              :   show this help
    + <txt> <:tag>  :   add a new todo (++ to add but not show list)
    x <ref>         :   mark as done/closed
    n <ref> note    :   add note to todo
    ... <txt> <:tag>:   update todo
    ^<ref> <txt>..  :   update todo
    = <txt>         :   search for matching todos
    =               :   show list of tags
    x               :   show closed

    use (daily) to create a daily repeating task
""")


def grant_user_request(todos):
    request = " ".join(sys.argv[1:])

    if request == "-h" or request == "--help":
        show_help()
        return

    if request == 'd':
        request = '=(daily)'

    resp = grant_request(request, todos)

    if not request:
        showShort(resp)
        showTot(todos)
        return

    if request == "=":
        show(resp["tags"])
        showShort(resp["untagged"])
        return

    if request[0] == "=":
        if len(resp) > 3:
            showShort(resp)
        else:
            show(resp)
        return

    if request[0] == "+":
        if len(request) == 1:
            return;
        if request[1] == "+":
            showShort(resp)
        else:
            showShort(showable(todos))
        update_file(resp)
        return

    if request[0] == "x":
        if not isinstance(resp, list):
            resp = [ resp ]
        for r in resp:
            if isinstance(r, ToDo):
                update_file(r)
        todos = load_todos()
        showShort(showable(todos))
        showTot(todos)
        for r in resp:
            show_closed(r)
        return

    if request[0] == '.':
        showShort(resp.repl)
        showShort(resp)
        update_file(todos)
        return

    if request[0] == '^':
        if isinstance(resp, list):
            if not resp:
                return
            for todo in resp:
                update_file(todo)
            show(showable(load_todos()))
            show(resp.repl)
        else:
            update_file(resp)
            show(showable(load_todos()))
            show(resp.repl)
        return

    if request[0] == 'n':
        show(resp)
        update_file(resp)
        return

def grant_request(request, todos):

    if not request:
        return showable(todos)

    if request == "=":
        return tagsAndUntagged(todos)

    if request[0] == "=":
        return get_filtered(todos, request[1:])

    if request[0] == "+":
        if len(request) == 1:
            return;
        if request[1] == "+":
            return add_new_todo(request[2:], todos)
        else:
            return add_new_todo(request[2:], todos)

    if request[0] == "x":
        return close(request[1:], todos)

    if request[0] == '.':
        return update(request, todos)

    if request[0] == '^':
        return update(request[1:], todos)

    if request[0] == 'n':
        return add_note(request[1:], todos)

    raise TTError("Did not understand " + request)


#       understand/
# when we are working on a todo, it moves to the
# head of the queue (last saved line in the file)
# Then we may want to add notes to this todo. Because
# every note updates the todo, we end up rewriting
# the entire todo each time.
# An easy optimization is to check for this case and
# only write the updated note line
#       example/
# - do something
# - and something
# with note
#                   (after adding a note line becomes)
# - do something
# - and something
# with note
# - and something
# with note
# another note
#                   (after adding more note lines becomes)
# - do something
# - and something
# with note
# - and something
# with note
# another note
# - and something
# with note
# another note
# one more note line
# - and something
# with note
# another note
# one more note line
# yet another note line
# - and something
# with note
# another note
# one more note line
# yet another note line
# we don't need to keep repeating this
#
#       way/
# to optimize this we check what the last todo
# looked line against the current todo and if
# it simply being extended then output the
# extension
def update_file(todo):
    if not todo or not todo.dirty:
        return

    with open(TODO_FILE, 'a') as f:
        if todo.repl and todo.repl.ref == 1:
            last = save_format(todo.repl)
            curr = save_format(todo)
            if curr.startswith(last):
                curr = curr[len(last):].strip()
                f.write(curr + "\n")
            else:
                f.write(save_format(todo) + "\n")
        else:
            f.write(save_format(todo) + "\n")


def add_note(request, todos):
    num, note = get_ref(request)
    if num == 0:
        raise TTError("Could not find reference for note")
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo = ToDo(todo_)
            todo.notes.append(note)
            todo.dirty = True
            todo.ref = 1
            todos.append(todo)
            return todo
    raise TTError("Could not find previous todo for note")

#       understand/
# we can reference todos using a "dotted notation":
#   .  < first/most recent todo
#   .. < second todo
#   ... < third todo
#   .... and so on
def get_dotted_ref(request):
    num = 0
    while request and request[0] == '.':
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
    request = request.strip()
    if request[0] == '.':
        return get_dotted_ref(request)
    elif request[0] == '^':
        return get_numbered_ref(request[1:])
    else:
        return get_numbered_ref(request)

def close(request, todos):
    if not request or not request.strip():
        return filter_closed(todos)
    else:
        return close_todos(request, todos)

def close_todos(request, todos):
    requests = request.split(",")
    resp = []
    for request in requests:
        request = request.strip()
        if request:
            resp.append(close_todo(request, todos))
    for r in resp:
        append_todo(r, todos)
    return resp

def close_todo(request, todos):
    num, request = get_ref(request)
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo = ToDo(todo_)
            if request:
                todo.notes.append(request)
            todo.closed = True
            todo.date = datetime.now(timezone.utc)
            todo.dirty = True
            break
    return todo

def update(request, todos):
    if request[0] == '=':
        return pull_up_matching(request[1:], todos)
    else:
        return update_one(request, todos)

def pull_up_matching(request, todos):
    todos_ = get_filtered(todos, request)
    return [update_todo(todo.ref, None, todos) for todo in todos_]

def update_one(request, todos):
    num, request = get_ref(request)
    return update_todo(num, request, todos)

def update_todo(num, txt, todos):
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo = ToDo(todo_)
            todo.date = datetime.now(timezone.utc)
            (txt, tags) = extract_tags(txt)
            if txt:
                todo.txt = txt
                todo.tags = tags
            todo.dirty = True
            append_todo(todo, todos)
            return todo
    raise TTError("Could not find previous todo")

def add_new_todo(txt, todos):
    id = 1
    for todo in todos:
        if todo.id >= id:
            id = todo.id + 1
    todo = make_todo(False, id, datetime.now(timezone.utc), txt)
    todo.dirty = True
    append_todo(todo, todos)
    return todo

def append_todo(todo, todos):
    for todo_ in todos:
        if not todo_.updated and not todo_.closed and todo_.ref:
            todo_.ref += 1
    todos.append(todo)
    todo.ref = 1

def make_todo(closed, id, date, txt):
    todo = ToDo()
    (todo.txt, todo.tags) = extract_tags(txt)
    todo.id = id
    todo.closed = closed
    todo.date = date
    return todo


def extract_tags(txt):
    if not txt or not txt.strip():
        return (txt,[])
    txt = txt.strip()
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
        if not todo.updated and todo.ref == num:
            return todo

class ToDo:
    def __init__(self, orig=None):
        if orig is None:
            self.construct()
        else:
            self.copy(orig)

    def copy(self, orig):
        self.id = orig.id
        self.ref = orig.ref
        self.txt = orig.txt
        self.tags = orig.tags[:]
        self.notes = orig.notes[:]
        self.date = orig.date

        self.updated = False
        self.closed = False
        self.dirty = False

        self.repl = orig
        orig.updated = True

    def construct(self):
        self.id = None
        self.ref = None
        self.txt = None
        self.tags = []
        self.notes = []
        self.date = None

        self.updated = False
        self.closed = False
        self.dirty = False

        self.repl = None

    def __repr__(self):
        closed = "x" if self.closed else "-"
        tags = ':'.join(self.tags)
        notes = '|'.join(self.notes)
        dirty = '*' if self.dirty else ""
        updated = 'XX' if self.updated else ""
        repl = f"^{self.repl.ref}" if self.repl else ""
        return f"ToDo<{updated}{closed}{self.id}{repl} {self.txt} :{tags}: #{self.ref} |{notes}| {dirty}{updated}>"


class TTError(Exception):
    pass


class TagStat:

    def __init__(self, tag):
        self.name = tag
        self.num = 1


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
    notes = "\n".join(["\t" + note for note in todo.notes])
    r = f"{ref} {closed}"
    if todo.txt:
        r = r + " " + todo.txt
    if tags:
        r = r + " " + tags
    if notes:
        r = r + "\n" + notes
    return r

def xpanded_format(todo):
    id = todo.id
    date = todo.date.astimezone().strftime('%a %b %d, %Y')
    closed = "x" if todo.closed else "-"
    tags = " ".join([f":{t}" for t in todo.tags])
    notes = "\n".join(["\t" + note for note in todo.notes])
    r = f"{closed}{id}"
    if todo.txt:
        r = r + " " + todo.txt
    if tags:
        r = r + " " + tags
    r = f"{r}\t({date})"
    if notes:
        r = r + "\n" + notes
    return r

def display_tag_stat(tagstat):
    return f"{tagstat.num:< 8}:{tagstat.name}"

def show_closed(todos):
    if not todos:
        print("")
        return
    if isinstance(todos, ToDo):
        todos = [todos]
    for todo in sorted(todos, key=lambda t: t.date):
        print(xpanded_format(todo))

def show(items):
    if not items:
        print("")
        return
    if not isinstance(items, list):
        items = [items]

    for item in items:
        if isinstance(item, TagStat):
            print(display_tag_stat(item))
        else:
            print(display_format(item))

def showTot(todos):
    mx = 0;
    for todo in todos:
        if todo.updated or todo.closed:
            continue
        if todo.ref > mx:
            mx = todo.ref
    if mx:
        print("/"+str(mx))

def showShort(items):
    if not items:
        print("")
        return
    if not isinstance(items, list):
        items = [items]
    show([short(t) for t in items])

def short(todo):
    if not todo.notes:
        return todo
    notes = [n for n in todo.notes if n.startswith("**")]
    if not notes:
        notes = todo.notes[0:2]
    n = len(todo.notes) - len(notes)
    if n > 0:
        notes.append(f"...{n} more")
    todo.notes = notes
    return todo


def showable(todos):
    return [todo for todo in todos if not todo.updated and not todo.closed]

def filter_closed(todos):
    return [todo for todo in todos if not todo.updated and todo.closed]

def get_filtered(todos, s):
    if not s:
        return []
    words = s.strip().split(" ")
    words = [w.lower() for w in words]
    return [todo for todo in showable(todos) if matches_1(words, todo)]

#       way/
# check that words are found in text or tags
# and -words are NOT found in text or tags
def matches_1(words, todo):
    minuswords = [word[1:] for word in words if word[0] == "-"]
    words = [word for word in words if word[0] != "-"]

    def found_1(word):
        if todo.txt and word in todo.txt.lower():
            return True
        if todo.tags:
            for tag in todo.tags:
                if word in f":{tag.lower()}":
                    return True
        return False

    for word in words:
        if not found_1(word):
            return False
    for word in minuswords:
        if found_1(word):
            return False
    return True

def tagsAndUntagged(todos):
    tagged = []
    untagged = []

    def add_tag_1(tag):
        for tagstat in tagged:
            if tagstat.name == tag:
                tagstat.num += 1
                return
        tagged.append(TagStat(tag))

    for todo in showable(todos):
        if todo.tags:
            for tag in todo.tags:
                add_tag_1(tag)
        else:
            if "(daily)" not in todo.txt.lower():
                untagged.append(todo)
    import operator
    return {
            "tags": sorted(tagged, key=operator.attrgetter('num','name'), reverse=True),
            "untagged": untagged
           }



if __name__ == "__main__":
    main()
