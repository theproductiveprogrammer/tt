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


  Scenario: Add a new todo item
    Given we have no todo items
     When we give the command "+ new item :123"
      And we give the command "+ another new item :123"
      And we give the command "n. note"
      And we give the command "+ next item IS THE BEST"
      And we give the command "x .."
    Then todo item 1 will have text "another new item"
     And todo item 1 will have tags "123"
     And todo item 1 will be marked dirty
     And todo item 1 will be closed 1
     And todo item 1 will have note "note"
     And todo item 2 will be closed 0
