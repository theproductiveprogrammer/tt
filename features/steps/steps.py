from behave import *
from tt import grant_request, add_new_todo, get_todo_item

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

@when(u'we give the command "{text}"')
def step_impl(context, text):
    grant_request(text, context.todos)


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
    print(todo.tags)
    assert not todo.tags

@then(u'todo item {num:d} will have tags "{tags}"')
def step_impl(context, num, tags):
    todo = get_todo_item(context.todos, num)
    assert tags == ",".join(todo.tags)
