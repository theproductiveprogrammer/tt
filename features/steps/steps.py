from behave import *
from tt import grant_request

@given(u'we have no todo items')
def step_impl(context):
    context.todos = []
    pass


@when(u'we give the command "{text}"')
def step_impl(context, text):
    grant_request(text, context.todos)


@then(u'the todo item {num:d} will have text "{text}"')
def step_impl(context, num, text):
    assert context.todos[num-1].txt == text

