# Task AuxSQLGenerator

The aim of this task/project is to write a python SQL generator that can be used to generate SQL statements for the
transformation of semi-structured data to structured data.

The task is not to write the SQL code itself, but to write a python script, which generates the SQL code.


## Setup of project

- Install docker with docker compose on your system, e.g. Docker Desktop for Windows will be sufficient
- Run `docker compose up` to start the docker containers (or the equivalent in Docker Desktop), this will start
  - a postgres instance and
  - a 'schema-server' instance
- Install a local python environment with poetry (see [this link](https://python-poetry.org/docs/) for details about installation and usage of poetry)
- Run the script 'init_db.py' in the python environment to initialize the database. This script creates the table 'raw_data' and fills in some dummy data.


## Task

- Write a python script, which:
  - get the newest version of the `user_created` schema from the schema server
  - generates the SQL statements to transform the data (see the requirements below for details) based on the schema
  - executes the SQL statements on the database


## Requirements

- The script should be written in python.
- The `data` column of the `raw_data` table should be flattened. That is, each attribute of the `data` column should become a column in the final table, so the final table should have the following columns:
  - id
  - aux_user_id
  - name
  - birthday
  - created_at
- Date attributes should be converted to the postgres date type.
- Timestamp attributes should be converted to the postgres timestamp with timezone type. All timestamps should be stored in UTC.
- The transformed data should be written into a new table `transformed_data` in the database.
- It should be easy to adapt the script to additional data types (here only four data types are used, however, in a bigger context another data type will be used like floats, decimals, etc.)
- The script should handle new data added to the `raw_data` table. That is, if new data is added to the `raw_data` table, the script should be able to transform the new data to the final table without changing the script.


### Optional requirements

- The script should handle the case, when duplicated entries are present in the raw data, that is when an 
  entire entry/row is inserted a second time into the raw table. The duplicated entries should not be added to the 
  transformed table. The script should be able to handle this case without changing the script.
- Write unit tests for the script.
- Write integration tests for the script.

## Details

### Raw data

The raw data has the following form and is located in the table 'raw_data' after the initialization of the database:

| id | data                                                                                                                         |
|----|------------------------------------------------------------------------------------------------------------------------------|
| 1  | {"aux_user_id": 4825155, "name": "Christopher Robles", "birthday": -17998, "created_at": "2020-09-21T08:35:23.107028+02:00"} |
| 2  | {"aux_user_id": 4997259, "name": "Cory Brown", "birthday": 12622, "created_at": "2023-05-11T14:24:01.020864+02:00"}          |
|    |                                                                                                                              |

The data column is of the json Postgres type. The structure of the json is described in the avro schema definition file,
which can be downloaded from the schema server. For details about the avro schema specification see
[this link](https://avro.apache.org/docs/1.11.1/specification/).

Additional remarks about the data:
- `aux_user_id` is a unique id for each user.
- `birthday` is the number of days since 1970-01-01.
- `created_at` is a ISO 8601 timestamp string with Europe/Berlin timezone.


### Schema Server

The schema server is a simple http server, which serves the avro schema definition file for the raw data. After
the container is started with docker compose, the OpenAPI documentation of the schema server can be found at
http://localhost:8000/docs, which describes the endpoints of the schema server.


### Postgres database

The postgres database is a simple postgres database, which is started with docker compose.
The database can be accessed with the following connection details:
- host: localhost
- port: 5432
- database: postgres
- user: postgres
- password: postgres

The database is initialized with the script 'init_db.py' in the python environment. The script creates the table
'raw_data' (in the `postgres.public` schema) and fills in some dummy data.