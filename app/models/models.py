"""
Define DB Models
"""

import enum

from flask_sqlalchemy import SQLAlchemy


class Direction(enum.Enum):

    """
    Define possible options for robot's facing directions
    """

    EAST = 0
    WEST = 1
    SOUTH = 2
    NORTH = 3


db = SQLAlchemy()


class Robot(db.Model):

    """
    Define the Robot database model (table)
    """

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.Enum(Direction), nullable=False)

    def __repr__(self):
        return f"Robot(id = {self.id}, x = {self.x}, y = {self.y}, direction = {self.direction})"


class Dino(db.Model):

    """
    Define the Dinosaur database model (table)
    """

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Dinosaur(id = {self.id}, x = {self.x}, y = {self.y})"


class Game(db.Model):

    """
    Define the Game grid database model (table)
    """

    id = db.Column(db.Integer, primary_key=True)
    dim = db.Column(db.Integer, default=50)
    n_robots = db.Column(db.Integer, default=0)
    n_dinos = db.Column(db.Integer, default=0)
    n_destroyed_dinos = db.Column(db.Integer, default=0)

    def __repr__(self):
        return (
            f"Game(dim = {self.dim}, n_robots = {self.n_robots},"
            + f"n_dinos = {self.n_dinos}, n_destroyed_dinos = {self.n_destroyed_dinos})"
        )
