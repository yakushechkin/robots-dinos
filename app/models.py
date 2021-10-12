from flask_sqlalchemy import SQLAlchemy

import enum

# from datetime import datetime


class Direction(enum.Enum):
    east = 0
    west = 1
    south = 2
    north = 3


db = SQLAlchemy()


class Robot(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.Enum(Direction), nullable=False)

    def __repr(self):
        return f"Robot(id = {id}, x = {x}, y = {y}, direction = {direction})"


class Dino(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def __repr(self):
        return f"Dinosaur(id = {id}, x = {x}, y = {y})"


class Game(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    dim = db.Column(db.Integer, default=50)
    n_robots = db.Column(db.Integer, default=0)
    n_dinos = db.Column(db.Integer, default=0)
    n_destroyed_dinos = db.Column(db.Integer, default=0)

    def __repr(self):
        return f"Game(dim = {dim}, n_robots = {n_robots}, n_dinos = {n_dinos}, n_destroyed_dinos = {n_destroyed_dinos})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
