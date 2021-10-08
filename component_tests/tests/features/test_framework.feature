Feature: This scenarios only test that producer and consumer of events in behave tests are implemented correctly

  Scenario: Send events and verify they arrived disregarding order
    Given Profile of Popeye with user id user_1
    And I am user Popeye

    When Sending event to weather topic
      | outside | rainy |
    And Sending event to weather topic
      | outside | sunny |
    And Sending event to weather topic
      | outside | snowing |

    Then Event on topic weather is expected to be emitted
      | outside | snowing |
    And Event on topic weather is expected to be emitted
      | outside | rainy |
    And Event on topic weather is expected to be emitted
      | outside | sunny |

    And Assert events arrived


  Scenario: Send events and and check that some other events are not present
    Given Profile of Popeye with user id user_1
    And I am user Popeye
    When Sending event to weather topic
      | outside | cold |
    Then Event on topic weather is not emitted
      | outside | hot |
    And Assert events arrived


  Scenario: Send events in multiple topics
    Given Profile of Popeye with user id user_1
    And I am user Popeye

    When Sending event to phrases topic
      | greeting | hello |
    And Sending event to cuisine topic
      | lunch | hamburger |
    And Sending event to phrases topic
      | greeting | bonjur |

    Then Event on topic phrases is expected to be emitted
      | greeting | hello |
    And Event on topic phrases is expected to be emitted
      | greeting | bonjur |
    And Event on topic cuisine is expected to be emitted
      | lunch | hamburger |

    And Assert events arrived

