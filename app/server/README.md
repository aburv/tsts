![Generic badge](https://img.shields.io/badge/Build-PASSED-green.svg)  ![Generic badge](https://img.shields.io/badge/Coverage-100%25-green.svg) ![Generic badge](https://img.shields.io/badge/Language-Python-green.svg)

# Data services
   A flask application

## Development server

### Prerequisites:
* Env configs
```
source envs/server.env
source envs/db.env
source FLASK_APP=src.app
```

* Install Dependencies
```
pip install -r requirements.txt
```

Run dev server.

`flask run`

```
http://localhost:5000/
```

## Happy Server coding

## Testing
### Unit Testing
Unit tests are present in Unit_tests/ folder. 
Controller and service level testing.
## Integration Testing
Integration tests are present in Integration_tests/ folder.
It tests the three layers (Controller -> Service -> DB)