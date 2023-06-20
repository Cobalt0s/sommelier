Feature: Example, check microservice makes external calls

  Scenario: External calls
    Given Define mock on POST /callback with status 200
    And mock with request
      | deliveryId | 123       |
      | type       | fulfilled |
    And mock must be called 1 times
    And end of mock definition
    Given Define mock on POST /callback with status 200
    And mock with request
      | deliveryId | 456     |
      | type       | started |
    And mock must be called 1 times
    And end of mock definition
    # now imitate external call which microservice should make
    When Make external call
      | deliveryId | 123       |
      | type       | fulfilled |
    Then Response status is ok
    When Make external call
      | deliveryId | 456     |
      | type       | started |
    Then Response status is ok
    Then All service mocks are satisfied
