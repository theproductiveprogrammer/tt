Feature: can parse saved todo items

  Scenario Outline: Parse a todo line
    Given we have no todo items
     When we parse the item "<item>"
     Then todo item 1 will have id <id>
      And todo item 1 will have date "<date>"
      And todo item 1 will have text "<text>"
      And todo item 1 will have tags "<tags>"
      And todo item 1 will be <closed>

    Examples:
      | item                                                             | id | date                             | text          | tags           | closed |
      | - 123@2022-01-01T02:03:35.897732+00:00 Check Prices :car         | 123| 2022-01-01T02:03:35.897732+00:00 | Check Prices  | car            | 0      |
      | - 1@2020-11-21T14:59:59.999999+00:00 Buy Cheese :shopping :store | 1  | 2020-11-21T14:59:59.999999+00:00 | Buy Cheese    | shopping,store | 0      |
      | x 19@2022-01-01T02:03:35.897732+00:00 Aquire Twitter :44bil      | 19 | 2022-01-01T02:03:35.897732+00:00 | Aquire Twitter| 44bil          | 1      |


  Scenario: Parse a set of items
    Given an existing todo list
      """
      - 34@2022-01-01T02:03:35.897732+00:00 Buy Car
      - 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 1 will have text "Code"
     And todo item 1 will have tags "tt"
     And todo item 1 will have id 36
     And todo item 2 will have text "Target"
     And todo item 2 will have tags "shopping"
     And todo item 2 will have id 35
     And todo item 3 will have text "Buy Car"
     And todo item 3 will have tags ""
     And todo item 3 will have id 34

  Scenario: Parse a set of items
    Given an existing todo list
      """
      - 34@2022-01-01T02:03:35.897732+00:00 Buy Car
      note1 note11
      note2 note22
      note4 note 44
      - 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 3 will have text "Buy Car"
     And todo item 3 will have tags ""
     And todo item 3 will have id 34
     And todo item 3 will have note "note1 note11|note2 note22|note4 note 44"
