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
    if request and request[0] == "+":
        todo = ToDo()
        todo.txt = request[1:].strip()
        todo.dirty = True
        todo.id = 1
        for todo_ in todos:
            if todo_.id == todo.id:
                todo.id += 1
        todos.append(todo)
    else:
        raise "Did not understand " + request

class ToDo:
    def __init__(self):
        self.id = None
        self.txt = None
        self.dirty = False


if __name__ == "__main__":
    main()
