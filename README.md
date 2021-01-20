# Flask App Test

This repository contains a Flask-based user dataset management application.

## Starting the server
`python run.py`

By default the server will run at `http://127.0.0.1:5000/`.

## API endpoints
* User login: `/api/dm/login`
* Data files: `/api/dm/datafiles`
* Data file details: `/api/dm/datafiles/<id>`

Some sample requests and responses are provided in the `DATA` folder.

## Running tests
`python tests.py`
