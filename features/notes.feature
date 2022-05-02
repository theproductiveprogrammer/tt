Feature: add and update notes

  Scenario: Add notes to todo item
    Given we have no todo items
     When we give the command "+ new item :123"
      And we give the command "n. new item IS THE BEST"
     Then todo item 1 will have id 1
      And todo item 1 will have note "new item IS THE BEST"
