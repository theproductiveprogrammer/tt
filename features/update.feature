Feature: update existing todos

  Scenario: Update an existing item
    Given we have 25 todo items
     When we give the command "+ another new item :123"
      And we give the command ". updated item :345"
     Then todo item 1 will have text "updated item :345"
      And todo item 1 will have id 26

