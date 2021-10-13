[![Build Status](https://github.com/yakushechkin/robots-dinos/actions/workflows/main.yml/badge.svg)](https://github.com/yakushechkin/robots-dinos/actions/workflows/main.yml)




# The 'robots-vs-dinos' challenge solution

Task: Implement a service that provides a REST API to support the simulation of remote-controlled robots to fight dinosaurs.

This REST API was built with Python 3.7, Flask, SQLAlchemy and Python standard library.

[API Documentation](https://app.swaggerhub.com/apis-docs/yakushechkin/Robots_vs_dinosaurs/1.0.0#/)

## Quick setup

Dependencies:  Python 3.7, pylint, black, flask, flask_restful, flask_sqlalchemy, pylint-flask-sqlalchemy

Create virtual environment in cloned/downloaded repository and install required packages.

```
python3 -m venv robotsdinos
source robotsdinos/bin/activate
make install
```

After activating virtual environment, tests can be run:

```
make test
```

Run the app:
```
python3 run.py
```

## Project structure:

- In the directory `/app`, you may find Database models (`models.py`), Resources (`game.py`, `robots.py`, `dinos.py`) and helper funtions (`utils.py`).
- In the directory `/test`, you will find the unit and integration tests.


## These are the features:

- Create an empty simulation space - an empty grid (default 50 x 50);
- Create a robot in a certain position and facing direction;
- Create a dinosaur in a certain position;
- A robot can turn left, turn right, move forward, move backward, and attack;
- A robot attack destroys dinosaurs around it (in front, to the left, to the right or behind);
- No need to worry about the dinosaurs - dinosaurs don't move;
- Display the simulation's current state;
- Two or more entities (robots or dinosaurs) cannot occupy the same position;
- Attempting to move a robot outside the simulation space is an invalid operation.
