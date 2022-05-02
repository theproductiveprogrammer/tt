#!/usr/bin/env python3
import sys
import os

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
        return parse_todos(f)

#       way/
# for each line in the file, parse it as a
# todo, blitzing the previous todo (if any)
# it is updating (and copying it's notes across)
# or adding the line as a note to the current
# todo
#       understand/
# The todo file format:
# - [id] text :tag :tag :tag
# x [id] text :tag :tag :tag
# associated notes
def parse_todos(lines):
    todos = []
    for line in lines:
        todo = parse_line(line)
        if todo is None:
            todo = todos[-1] if todos else ToDo()
            todo.addNote(line)
        else:
            for todo_ in reversed(todos):
                if todo_.id == todo.id:
                    todo_.closed = True
                    todo.notes = todo_.notes
                    break
            todos.append(todo)
    return todos

def parse_line(line):
    return None

def grant_user_request(todos):
    print(todos)

def grant_request(request, todos):
    if not request:
        raise "Nothing to do!"

    if request[0] == "+":
        add_new_todo(request[1:], todos)
    elif request[0] == '.':
        update_dotted(request, todos)
    else:
        raise "Did not understand " + request


#       understand/
# we can reference todos using a "dotted notation":
#   .  < first/most recent todo
#   .. < second todo
#   ... < third todo
#   .... and so on
def update_dotted(request, todos):
    num = 0
    while request[0] == '.':
        num += 1
        request = request[1:]
    update_todo(num, request, todos)

def update_todo(num, txt, todos):
    todo = make_new_todo(txt, todos)
    for todo_ in reversed(todos):
        if todo_.ref == num:
            todo.id = todo_.id
        todo_.ref += 1
    append_todo(todo, todos)

def add_new_todo(txt, todos):
    append_todo(make_new_todo(txt, todos), todos)

def append_todo(todo, todos):
    for todo_ in todos:
        todo_.ref += 1
    todos.append(todo)

def make_new_todo(txt, todos):
    todo = ToDo()
    todo.txt = txt.strip()
    if not todo.txt:
        raise "Todo item empty"
    todo.dirty = True
    todo.id = 1
    todo.ref = 1
    for todo_ in todos:
        if todo_.id == todo.id:
            todo.id += 1
    return todo

def get_todo_item(todos, num):
    for todo in reversed(todos):
        if todo.ref == num:
            return todo

class ToDo:
    def __init__(self):
        self.id = None
        self.ref = None
        self.txt = None
        self.dirty = False

    def __repr__(self):
        return f"ToDo<{self.id} {self.txt} #{self.ref} {'*' if self.dirty else None}>"

if __name__ == "__main__":
    main()
