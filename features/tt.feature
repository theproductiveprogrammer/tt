Feature: tt todo manager

  Scenario Outline: Add a new todo item
    Given we have no todo items
     When we give the command "<cmd>"
     Then todo item 1 will have text "<text>"
      And todo item 1 will be marked dirty

    Examples:
      | cmd           |   text     |
      | + new item    | new item   |
      | +new item     | new item   |
      | +  new item   | new item   |
      | +  NEW Item   | NEW Item   |


  Scenario: Add a new todo item
    Given we have no todo items
     When we give the command "+ another new item :123"
     Then todo item 1 will have id 1

  Scenario: Add a new todo item
    Given we have no todo items
     When we give the command "+ another new item :123"
      And we give the command "+ next item IS THE BEST"
     Then todo item 1 will have id 1
      And todo item 2 will have id 2
