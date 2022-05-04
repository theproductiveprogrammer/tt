Feature: close completed todos

  Scenario: Add a new todo item
    Given we have no todo items
     When we give the command "+ new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ next item IS THE BEST"
      And we give the command "x ."
     Then todo item 1 will have text "next item IS THE BEST"
      And todo item 1 will be marked dirty
      And todo item 1 will be closed 1
