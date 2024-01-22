# Task AuxSQLGenerator

The aim of this task is to write a python SQL generator that can be used to generate SQL statements for the
transformation of semi-structured data to structured data.

The task is not to write the SQL code itself, but to write a python script, which generates the SQL code.


## Setup of project

1. Install docker with docker compose on your system, e.g. Docker Desktop for Windows will be sufficient 
2. Install a local python environment with poetry (see [this link](https://python-poetry.org/docs/) for details about installation and usage of poetry)
3. Run `docker compose up` to start the docker containers (or the equivalent in Docker Desktop), this will start
   - a Postgres instance and
   - a 'schema-server' instance
4. Run the script `init_db.py` in the python environment to initialize the database. This script creates the table 'raw_data' and fills in some dummy data.


## Task

- Write a python script, which:
  - gets the newest version of the `user_created` schema from the schema server
  - generates the SQL statements to transform the data based on the schema (see the requirements below for details)
  - executes the SQL statements on the database


## Requirements

- The script should be written in python.
- The `data` column of the `raw_data` table should be flattened. Therefore, each attribute of the `data` column should be unpacked into its own column in the final table. The final table should have the following columns:
  - id
  - aux_user_id
  - name
  - birthday
  - created_at
- Date attributes should be converted to the Postgres date type.
- Timestamp attributes should be converted to the Postgres timestamp with timezone type. All timestamps should be stored in UTC.
- The transformed data should be written into a new table `transformed_data` in the database.
- It should be easy to adapt the script to additional data types (here only four data types are used, however, in a bigger context other data types will be used like floats, decimals, etc.)
- The script should handle new data added to the `raw_data` table. Hence, if new data is added to the `raw_data` table, the script should be able to transform the new data and load it to the final table.


### Optional requirements

1. Duplicate entries in `raw_data` should be de-duplicated during the load to the `transformed_data` table. Duplicated 
   entries in this context are when an entire entry/row is inserted a second time into the raw table.
2. Write unit tests for the script.
3. Write integration tests for the script.

## Details

### Raw data

The raw data has the following form and is located in the table `raw_data` after the initialization of the database:

| id | data                                                                                                                         |
|----|------------------------------------------------------------------------------------------------------------------------------|
| 1  | {"aux_user_id": 4825155, "name": "Christopher Robles", "birthday": -17998, "created_at": "2020-09-21T08:35:23.107028+02:00"} |
| 2  | {"aux_user_id": 4997259, "name": "Cory Brown", "birthday": 12622, "created_at": "2023-01-11T14:24:01.020864+01:00"}          |

The data column is of the json Postgres type. The structure of the json is described in the avro schema definition file,
which can be downloaded from the schema server. For details about the avro schema specification see
[this link](https://avro.apache.org/docs/1.11.1/specification/).

Additional remarks about the data:
- `aux_user_id` is a unique id for each user.
- `birthday` is the number of days since 1970-01-01.
- `created_at` is a ISO 8601 timestamp string with Europe/Berlin timezone.


### Schema Server

The schema server is a simple http server that serves the avro schema definition file for the raw data. After
the container is started with docker compose, the OpenAPI documentation of the schema server can be found at
http://localhost:8000/docs, which describes the endpoints of the schema server.


### Postgres database

The Postgres database is a simple Postgres database, which is started with docker compose.
The database can be accessed with the following connection details:
- host: localhost
- port: 5432
- database: postgres
- user: postgres
- password: postgres

The database is initialized with the script `init_db.py` in the python environment. The script creates the table
`raw_data` (in the `postgres.public` schema) and fills in some dummy data.