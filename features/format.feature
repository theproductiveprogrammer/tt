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

  Scenario: Represents a todo in a save-able format
    Given an existing todo list
      """
      - 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 2 will have save format
      """
      - 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """

  Scenario: Represents a todo in a save-able format
    Given an existing todo list
      """
      - 34@2022-01-01T02:03:35.897732+00:00 Buy Car
      note1 note11
      note2 note22

      note4 note 44
      - 35@2022-01-01T02:03:35.897732+00:00 Target
      - 36@2022-01-01T02:03:35.897732+00:00 :shopping :hi
      """
    When we give the command "+ Code :tt"
    Then todo item 3 will have save format
      """
      - 35@2022-01-01T02:03:35.897732+00:00 Target
      """
     And todo item 2 will have save format
      """
      - 36@2022-01-01T02:03:35.897732+00:00 :shopping :hi
      """

  Scenario: Represents a todo in a save-able format
    Given an existing todo list
      """
      x 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 2 will have save format
      """
      x 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """

  Scenario: Represents a todo in a display-able format
    Given an existing todo list
      """
      x 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    When we give the command "+ Code :tt"
    Then todo item 2 will have display format
      """
      [.   ]x Target :shopping
      """

