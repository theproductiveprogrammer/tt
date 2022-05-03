from behave import *
from tt import grant_request, add_new_todo, get_todo_item, parse, parse_line, save_format, display_format
from datetime import *

@given(u'we have no todo items')
def step_impl(context):
    context.todos = []
    pass

@given(u'we have {num:d} todo items')
def step_impl(context, num):
    context.todos = []
    for i in range(num):
        add_new_todo("item" + str(i), context.todos)
    pass

@given(u'an existing todo list')
def step_impl(context):
    context.todos = parse(context.text.split("\n"))
    num = 1
    for todo in reversed(context.todos):
        todo.ref = num
        num += 1



@when(u'we give the command "{text}"')
def step_impl(context, text):
    grant_request(text, context.todos)

@when(u'we parse the item "{text}"')
def step_impl(context, text):
    todo = parse_line(text)
    todo.ref = 1
    context.todos.append(todo)


@then(u'todo item {num:d} will have text "{text}"')
def step_impl(context, num, text):
    assert get_todo_item(context.todos, num).txt == text

@then(u'todo item {num:d} will be marked dirty')
def step_impl(context, num):
    assert get_todo_item(context.todos, num).dirty

@then(u'todo item {num:d} will have id {id:d}')
def step_impl(context, num, id):
    assert get_todo_item(context.todos, num).id == id

@then(u'todo item {num:d} will have tags ""')
def step_impl(context, num):
    todo = get_todo_item(context.todos, num)
    assert not todo.tags

@then(u'todo item {num:d} will have tags "{tags}"')
def step_impl(context, num, tags):
    todo = get_todo_item(context.todos, num)
    assert tags == ",".join(todo.tags)

@then(u'todo item {num:d} will have note "{notes}"')
def step_impl(context, num, notes):
    todo = get_todo_item(context.todos, num)
    assert notes == "|".join(todo.notes)

@then(u'todo item {num:d} will have date "{date}"')
def step_impl(context, num, date):
    date = datetime.fromisoformat(date)
    assert get_todo_item(context.todos, num).date == date

@then(u'todo item {num:d} will be 0')
def step_impl(context, num):
    assert (not get_todo_item(context.todos, num).closed)

@then(u'todo item {num:d} will be 1')
def step_impl(context, num):
    assert get_todo_item(context.todos, num).closed

@then(u'todo item {num:d} will have save format')
def step_impl(context, num):
    todo = get_todo_item(context.todos, num)
    assert save_format(todo) == context.text

@then(u'todo item {num:d} will have display format')
def step_impl(context):
    todo = get_todo_item(context.todos, num)
    assert display_format(todo) == context.text
