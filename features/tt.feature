Feature: tt todo manager

  Scenario Outline: Add a new todo item
    Given we have no todo items
     When we give the command "<cmd>"
     Then the todo item 1 will have text "<text>"
      And the todo item 1 will be marked dirty

    Examples:
      | cmd           |   text     |
      | + new item    | new item   |
      | +new item     | new item   |
      | +  new item   | new item   |

