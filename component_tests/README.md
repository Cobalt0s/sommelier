# Integration Tests using Cucumber and Python's Behave

This module contains a set of test suites which do _Behaviour Driven Testing_.

Run tests with:
`behave ./tests/tests.features/`

## Using `flask/scripts/test` Script

> **MAKE SURE YOU HAVE ACTIVATED THE VIRTUAL PYTHON ENVIRONMENT** <br>
> To do so, you can simply execute the following command under the root directory of `spicy-mango` > `$ . flask/env/bin/activate` > **_NOTE:_** To make sure this runs you will need to setup a python virtual environment under the `flask/` directory. Refer to the main `README` of spicy-mango for more details.

For efficient testing, the script `test` under scripts is provided. What this script does? you may ask. Here it is:

- Install `behave` using pip
- Spin up a new mongo docker container called `testdb` got testing purposes
- Load in the `testenv` variables (See **Test Env Variables** section for more details)
- Run the the tests using `behave`
- Remove `testdb` docker container and prune other unused docker objects/resources which might be present on your system

## Test Env Variables

To load in the test enviornment variables:

- Create a file called `testenv` under the `flask/scripts/` directory
- Provide executable permissions for `testenv`

```bash
$ chmod +x flask/scripts/testenv
```

- Add the following contents to `testenv`


## Using the `test` Script

We test `spicy-mango` tests.features by first running a live instance of our flask server and then execute tests which makes requests to the running flask server

To test flask server:

- Open a terminal and navigate to root directory of `spicy-mango` and activate the virtual enviornment
- Execute `flask/scripts/start` (Make sure you setup the env vars for the flask server. See main `README` for more details)
- Open a second terminal and navigate to root directory of `spicy-mango` and activate the virtual enviornment
- Execute the `flask/scripts/test` (Make sure to setup the testing env vars. See **Test Env Variables** section above)

## Special Syntax

### Object Id

The JSON response may include **id** field.

In order to use this value as an argument to other steps we can save this inside of the context and then later
reference using **\$** sign.

A random id can be generated using **\$#**. This can be useful when we want to provide an undefined id as part of a request.

See: _define_item_id_

### Data Tables

First row of data tables supports nested keys.
If we are dealing with nested components in json we can use **>>** symbol to zoom into the value.

Second row of data tables supports **ids** as well as arrays.
You can enclose values in **[]** like **[a, b]**.

### Query Params

There is a support of pagination query parameters.

## Test flow

### Reusing Response Data

We can do multiple requests and revisit them at later point by creating references.
By default, the latest call will be saved as **context.result**.

See: _save_reference_ to save response result for future reference.

See: _switch_context_to_reference_ in order to use previously saved response result.

### JSON utility methods

To check presence of values in JSON object see: _contains_ and _missing_ methods.


### Library Dependencies

Behave explanation https://automationpanda.com/2018/05/11/python-testing-101-behave/
