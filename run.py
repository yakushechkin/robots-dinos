# run.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # ORM
from flask_restful import Api

from config import Config

# import resources
from app.game import Game_resource
from app.robots import Robot_resource
from app.dinos import Dino_resource


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
# db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Robot_resource, "/robot/")
api.add_resource(Dino_resource, "/dino/")
api.add_resource(Game_resource, "/game/")


if __name__ == "__main__":
    from app.models import db

    db.init_app(app)
    app.run(port=5000, debug=True)
