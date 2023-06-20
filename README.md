
# 🍷 Sommelier
## Behave wrapper for testing microservices in python 🐍

## Check Examples to see testing setup and use cases

TODO [WIP]

## Features

* REST API calls to the service
* Mocking dependant service calls
* Kafka event
  * Consumption
    * Specify expected events, then assert
    * **TODO**: cucumber example
  * Production
    * Describe payload to send to kafka
    * **TODO**: cucumber example
* Validating JSON (from REST or Kafka) using dot separated keys and values in Cucumber table
    * **TODO**: cucumber example
* Declaring aliases from JSON response that comes from Kafka or REST
  * Scoped aliases
    * Permanent last the whole execution
      * **TODO**: cucumber example
    * Temporary are local for the feature lifecycle
      * **TODO**: cucumber example
  * Accessing variables with '$'
    * **TODO**: cucumber example
* SocketIO messages can be sent and received
    * **TODO**: standalone additional process does the work, provide link to it
    * **TODO**: cucumber example that calls the process
* Helpers
  * JsonRetriever
    * Goal: Behave table is in CSV format while we need to operate wit JSON under the hood 
    * Wrapper data structure that allows to access json with mixed dict keys and list indexes
      * Ex: data.customers.[3].name -> [3] is understood as accessing 4th object of data.customers list
  * Data table converters
    * Cucumber tables converted to dictionary (json), lists (columns)
    * Two columns: json key, json value
    * One column: json key, (allows checking key presence)
  * Assertions (equals/contains/missing)
    * **TODO**: cucumber example that calls the process

### TODO
* Page navigation
  * **TODO**: this is cursor based (should be customizable)
* Context Manager
  * TODO: example of Dependency Injection
  * TODO: variable scope management (permanent vs per-scenario scopes)
* Add Framework Tests
  * TODO CI automation
  * TODO tests various used versions if any
