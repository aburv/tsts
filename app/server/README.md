![Generic badge](https://img.shields.io/badge/Build-PASSED-green.svg)  ![Generic badge](https://img.shields.io/badge/Coverage-100%25-green.svg) ![Generic badge](https://img.shields.io/badge/Language-Python-green.svg)

# Data services

A flask application -V3.0.0

Python -V3.10

## Development server

### Prerequisites:

* Env configs
  setup the values

```commandline
source envs/server.env
source envs/db.env
source FLASK_APP=src.app
```

* Install Dependencies

```commandline
pip install -r requirements.txt
```

* Run local server.

```commandline
flask run
```

Check ` http://localhost:5000/ ` in any rest api client to test the response

Database client

```commandline
psql "dbname=<db_name> user=<db_user>"
```

to view the postgresql data in the terminal

## Code Quality

### Lint

```commandline
pylint src ./migrate_db.py 
```

Maintain 10.0

## Testing

### Unit Testing

Unit tests are present in Unit_tests/ folder.
Controller and service level testing.

## Integration Testing

Integration tests are present in Integration_tests/ folder.
It tests the three layers (Controller -> Service -> DB)

```commandline
coverage run --source=. -m unittest discover -s test 
coverage html
```

View Code Coverage in html format

`htmlcov/index.html`

## Happy Server coding