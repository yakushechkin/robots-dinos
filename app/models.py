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
    # created = db.Column(db.DateTime, default=datetime.now())

    # def __init__(self, *args, **kwards):
    #     super().__init__(*args, **kwards)
        
    def __repr(self):
        return f"Robot(id = {id}, x = {x}, y = {y}, direction = {direction})"

class Dino(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    # created = db.Column(db.DateTime, default=datetime.now())
       
    def __repr(self):
        return f"Dino(id = {id}, x = {x}, y = {y})"