# Database Versioner (dbv)
Database versioner to be used to version Postgres &amp; Redshift

## Features

  * Able to run db migrations in a single command
  * Manages current version of the database
  * Able to randomize password and store in AWS SSM
  * Useful for CICD deployments
  * Better than sharing data dump exports

## Installation

This is a [python](https://www.python.org/) module available through the
[pypi registry](https://pypi.org).

Before installing, [download and install python](https://www.python.org/downloads/).
python 3 or higher is required.

Installation is done using the
[`pip install`](https://packaging.python.org/tutorials/installing-packages/) command:

```bash
$ pip install syngenta_digital_dbv
```

or

```bash
$ pipenv install syngenta_digital_dbv
```

## Basic Usage

### Postgres/Redshift
```python
import syngenta_digital_dbv

def some_func():
    syngenta_digital_dbv.version(
        engine='postgres',
        endpoint='localhost',
        database='dbv-postgis',
        port=5433,
        user='root',
        password='Lq4nKg&&TRhHv%7z',
        ssm_param='local-postgres-config',
        versions_directory='application/db_versions/version_number_files',
        reset_root=True
    )
```

Option Name         | Required | Type   | Description
:-----------        | :------- | :----- | :----------
`engine`            | true     | string | name of supported db engine (postgres)
`endpoint`          | true     | string | url of your host db
`database`          | true     | string | name of the database to connect to
`port`              | true     | int    | port of database (no defaults)
`user`              | true     | string | root username for database access
`password`          | true     | string | root password for database access
`versions_directory`| true     | string | directory where all you files can be found
`ssm_param`         | false    | string | ssm param path you want to store your db configs
`reset_root`        | false    | boolean| whether to reset the root password; will ignore if ssm_param not defined
`seed`              | false    | boolean| whether to seed data (great for local development)
`seed_directory`    | false    | string | directory where all you files can be found

#### Postgres/Redshift Example File Contents

```sql
CREATE TABLE users_a (
    id SERIAL PRIMARY KEY,
    "user" text,
    password text
);
CREATE TABLE foods_a (
    id SERIAL PRIMARY KEY,
    name text,
    calories text
);
ALTER TABLE foods_a ADD COLUMN user_id int;
ALTER TABLE foods_a ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users_a (id) MATCH FULL;
```

*NOTE: File names must be unique and in order (i.e. 1.sql, 2.sql, etc or a.sql, b.sql, etc), this is how the package knows what order to run the files in*

### Mongo
```python
import syngenta_digital_dbv

def some_func():
    syngenta_digital_dbv.version(
        engine='mongo',
        database='unit',
        user='root',
        password='Lq4nKg&&TRhHv%7z',
        endpoint='mongodb://localhost:27017/',
        versions_directory='tests/mocks/mongo/version_number_files',
        seed=True,
        seed_directory='tests/mocks/mongo/seed'
    )
```

Option Name         | Required | Type   | Description
:-----------        | :------- | :----- | :----------
`engine`            | true     | string | name of supported db engine (postgres)
`endpoint`          | true     | string | url of your host db
`database`          | true     | string | name of the database to connect to
`user`              | true     | string | root username for database access
`password`          | true     | string | root password for database access
`versions_directory`| true     | string | directory where all you files can be found
`seed`              | false    | boolean| whether to seed data (great for local development)
`seed_directory`    | false    | string | directory where all you files can be found

#### Mongo Example File Contents

```json
[
    {
        "database": "unit",
        "collection": "test",
        "operation": "create_index",
        "query": "user_email",
        "params": {"background": true, "unique": true}
    },
    {
        "database": "unit",
        "collection": "test",
        "operation": "create_index",
        "query": [["first", 1], ["last", -1]],
        "params": {"name": "first_last"}
    }
]
```
*NOTE: Full list of collection operations found here: https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html*

*NOTE: Databases and collections are automatically by mongo; no need to have specific commands to create them*

*NOTE: File names must be unique and in order (i.e. 1.json, 2.json, etc or a.json, b.json, etc), this is how the package knows what order to run the files in*
