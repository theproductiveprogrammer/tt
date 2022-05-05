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
    Then todo item 1 will have save format
      """
      x 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """

  Scenario: Represents a todo in a display-able format
    Given an existing todo list
      """
      x 35@2022-01-01T02:03:35.897732+00:00 Target :shopping
      """
    Then todo item 1 will have display format
      """
      .    x Target :shopping
      """

  Scenario: Represents a todo in a display format
    Given an existing todo list
      """
      - 33@2022-01-01T02:01:35.897732+00:00 Create Program
      - 34@2022-01-01T02:02:35.897732+00:00 Buy Car
      note1 note11
      note2 note22

      note4 note 44
      - 35@2022-01-01T02:03:35.897732+00:00 Target
      - 36@2022-01-01T02:04:35.897732+00:00 :shopping :hi
      - 37@2022-01-01T02:05:35.897732+00:00 Code :tt
      """
    Then todo item 5 will have display format
      """
      5    - Create Program
      """
    Then todo item 4 will have display format
      """
      .... - Buy Car
      	note1 note11
      	note2 note22
      	
      	note4 note 44
      """
     And todo item 3 will have display format
      """
      ...  - Target
      """
     And todo item 2 will have display format
      """
      ..   - :shopping :hi
      """
     And todo item 1 will have display format
      """
      .    - Code :tt
      """


