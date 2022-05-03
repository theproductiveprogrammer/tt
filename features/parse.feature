Feature: can parse saved todo items

  Scenario: Parse a set of items
    Given an existing todo list
      """
      - [34] Buy Car
      - [35] Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 1 will have text "Code"
     And todo item 1 will have tags "tt"
     And todo item 1 will have id 36
