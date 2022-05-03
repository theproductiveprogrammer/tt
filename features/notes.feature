Feature: add and update notes

  Scenario: Add notes to todo item
    Given we have no todo items
     When we give the command "+ new item :123"
      And we give the command "n. new item IS THE BEST"
     Then todo item 1 will have id 1
      And todo item 1 will have note "new item IS THE BEST"

  Scenario: Append notes to todo item
    Given we have no todo items
     When we give the command "+ new item :123"
      And we give the command "n. 1"
      And we give the command "n. 2"
     Then todo item 1 will have id 1
      And todo item 1 will have note "1|2"

  Scenario: Copy existing notes to updated todo item
    Given we have no todo items
     When we give the command "+ first"
     When we give the command "+ item :123"
      And we give the command "n. 1"
      And we give the command "n. 2"
      And we give the command "+ another item"
      And we give the command "+ another item"
      And we give the command "+ another item"
      And we give the command "+ another item"
      And we give the command "+ another item"
      And we give the command "+ another item"
      And we give the command "^7 updated"
     Then todo item 1 will have id 2
      And todo item 1 will have text "updated"
      And todo item 1 will have note "1|2"
