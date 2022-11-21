
# Sommelier [WIP]
## Behave wrapper for testing microservices in python
Need to add customisation as now it just works for particular use case and not yet generalised.


## Features

* REST API calls to the service
* Mocking dependant service calls
  * ****TODO**** [WIP]
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
    * Special object that allows to access json with mixed dict keys and list indexes
  * Data table converters
    * Cucumber tables converted to dictionary (json), lists (columns)
  * Assertions (equals/contains/missing)
    * **TODO**: cucumber example that calls the process

### TODO
* Page navigation
  * **TODO**: this is cursor based (should be customizable)
* Context Manager
  * A lot of refactoring, all managers must use it as a 'Behave' context wrapper
* Add Examples
* Add Tests