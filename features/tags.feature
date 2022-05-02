Feature: extract item tags

  Scenario Outline: Add a new todo item
    Given we have no todo items
     When we give the command "<cmd>"
     Then todo item 1 will have tags "<tags>"

    Examples:
      | cmd                                   |   tags    |
      | + new item :123                       |  123      |
      | +new item :a :1bc :dwe                | a,1bc,dwe |
      | +  new item                           |           |
      | +  NEW Item :                         |           |
      | +  NEW Item :another-brick-on-the-fire| another-brick-on-the-fire |
      | +  NEW Item :another:brick :the-fire  | another,brick,the-fire    |

