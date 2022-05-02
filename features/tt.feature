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


  Scenario: Add a new todo item
    Given we have no todo items
     When we give the command "+ another new item :123"
     Then todo item 1 will have id 1
