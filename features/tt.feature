Feature: tt todo manager

  Scenario: Add a new todo item
    Given we have no todo items
     When we give the command "+ new item"
     Then the todo item 1 will have text "new item"

