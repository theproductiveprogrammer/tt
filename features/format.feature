Feature: show/represent the todo

  Scenario: Represents a todo in a save-able format
    Given an existing todo list
      """
      - 34@2022-01-01T02:03:35.897732+00:00 Buy Car
      note1 note11
      note2 note22

      note4 note 44
      - 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 3 will have save format
      """
      - 34@2022-01-01T02:03:35.897732+00:00 Buy Car
      note1 note11
      note2 note22

      note4 note 44
      """
