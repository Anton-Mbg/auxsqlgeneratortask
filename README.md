# Task AuxSQLGenerator

The aim of this task/project is to write a python SQL generator that can be used to generate SQL statements to transform
semi-structured data to structured data.

The task is not to write the SQL code itself, but to write a python script, which generates the SQL code.


## Setup of project

- Install docker with docker compose on your system
- Run `docker compose up` to start the docker containers, this will start
  - a postgres instance and
  - a 'schema-server' instance.
- Install a local python environment with poetry (see [this link](https://python-poetry.org/docs/) for details about installation and usage)
- Run the script 'init_db.py' in the python environment to initialize the database


## Task

- Write a python script, which:
  - gets the correct schema from the schema server
  - generates the SQL statements to transform the data (see the requirements below for details)
  - executes the SQL statements on the database


## Requirements

- The script should be written in python
- Date attributes should be converted to the postgres date type
- Timestamp attributes should be converted to the postgres timestamp with timezone type. All timestamps should be stored
  in UTC.
- It should be easy to adapt the script to additional avro data types


## Details

### Raw data

The raw data has the following form and is located in the table 'raw_data' after the initialization of the database:

| id | data                                                                                                                      |
|----|---------------------------------------------------------------------------------------------------------------------------|
| 1  | {"auxUserId": 4825155, "name": "Christopher Robles", "birthday": -17998, "createdAt": "2020-09-21T08:35:23.107028+02:00"} |
| 2  | {"auxUserId": 4997259, "name": "Cory Brown", "birthday": 12622, "createdAt": "2023-05-11T14:24:01.020864+02:00"}          |
|    |                                                                                                                           |

The data column is of the json Postgres type. The structure of the json is described in the avro schema definition file,
which can be downloaded from the schema server. For details about the avro schema specification see
[this link](https://avro.apache.org/docs/1.11.1/specification/).

### Schema Server

The schema server is a simple http server, which serves the avro schema definition file for the raw data. After
the container is started with docker compose, the OpenAPI documentation of the schema server can be found at
http://localhost:8000/docs.


### Postgres database

The postgres database is a simple postgres database, which is started with docker compose.
The database can be accessed with the following connection details:
- host: localhost
- port: 5432
- database: postgres
- user: postgres
- password: postgres

The database is initialized with the script 'init_db.py' in the python environment. The script creates the table
'raw_data' and fills in some dummy data.