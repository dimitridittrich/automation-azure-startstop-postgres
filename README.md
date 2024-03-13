# Start Stop Postgres
This repository contains Python code to automate the start/stop of Postgres Flexible Servers. <br>
Azure PostgreSQL flexible server allows you to stop and start the server on-demand to allow significant cost savings. <br>
The compute tier billing is stopped immediately when the server is stopped. <br>
Basically we have our main script, which is "src/implementation.py", which consumes all the others (src/postgre.py, src/subscriptions.py and src/util/logger.py).<br>
The automation reads all subscriptions defined in the "self.azure_subscriptions" block in the "src/subscriptions.py" file, lists all Flexible Posgres from these subscriptions, checks the "azuretag.environment" tag to filter only resources that belong to the **dev, stg** and **nonprod** environments.<br>
Checks the times defined in the azuretag.start and azuretag.stop tags and starts or stops the server if any of these tags have the same execution time as the defined script. Therefore, in Rundeck this automation runs every one hour.

## Requirements
Python:
- Version: >= 3.10
- Dependencies: [requirements.txt](./requirements.txt)

## Run automation
To run the automation on your machine, simply run the "app.py" file. It is not necessary to create a virtual environment or configure environment variables, as this automation fetches the necessary information via the Azure API.

## Run unit tests
We have three unit test files within "test/unit", which are:<br>
- test_implementation.py
- test_postgre.py
- test_subscription.py

To run the tests use pytest.

```sh
pytest 
```

## Check code coverage

```sh
coverage run -m pytest
coverage html
```

## Deploy

Currently this automation runs on a recurring and scheduled basis via Rundeck. However, the way it was structured allows it to be run from any other location as long as it allows the use of Python.
