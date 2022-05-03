Feature: update existing todos

  Scenario: Update an existing item
    Given we have 25 todo items
     When we give the command "+ another new item :123"
      And we give the command ". updated item :345"
     Then todo item 1 will have text "updated item"
      And todo item 1 will have id 26

  Scenario: Update an existing item
    Given we have 25 todo items
     When we give the command "+ another new item :123"
      And we give the command "+ new item :345"
      And we give the command ".. updated item :99"
     Then todo item 1 will have text "updated item"
      And todo item 1 will have id 26

  Scenario: Update an existing item
    Given we have 25 todo items
     When we give the command "+ another new item :123"
      And we give the command "+ new item :345"
      And we give the command ". updated item :99"
     Then todo item 1 will have text "updated item"
      And todo item 1 will have id 27

  Scenario: Update an existing item
    Given we have no todo items
     When we give the command "+ new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ another new item :123"
      And we give the command "+ new item :345"
      And we give the command ".... updated item :99"
     Then todo item 1 will have text "updated item"
      And todo item 1 will have tags "99"
      And todo item 1 will have id 8

  Scenario: Update an existing item
    Given we have 25 todo items
     When we give the command "+ another new item :123"
      And we give the command "^1 updated item :345"
     Then todo item 1 will have text "updated item"
      And todo item 1 will have id 26

  Scenario: Update an existing item
    Given we have 25 todo items
     When we give the command "+ another new item :123"
      And we give the command "^1 updated item :345"
      And we give the command "^1 another update"
     Then todo item 1 will have text "another update"
      And todo item 1 will have id 26

  Scenario: Update an existing item
    Given we have 100 todo items
     When we give the command "^100 updated item :99"
     Then todo item 1 will have text "updated item"
      And todo item 1 will have tags "99"
      And todo item 1 will have id 1

  Scenario: Update an existing item
    Given we have no todo items
     When we give the command "+ another new item :123"
     When we give the command "+ yet another item :123"
      And we give the command "^2 updated item :345"
      And we give the command "^2 another update"
     Then todo item 1 will have text "another update"
      And todo item 1 will have id 2
      And todo item 2 will have text "updated item"
      And todo item 2 will have tags "345"
      And todo item 2 will have id 1

  Scenario: Pull an existing item to the top
    Given we have no todo items
     When we give the command "+ another new item :123"
      And we give the command "+ a third item :456:123"
      And we give the command "+ yet another item :123"
      And we give the command "^2"
     Then todo item 1 will have id 2
      And todo item 1 will have text "a third item"
      And todo item 1 will have tags "456,123"

