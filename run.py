# run.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # ORM
from flask_restful import Api

from config import Config

# import resources
from app.robots import Robot_resource

# from resources.item import Item, ItemList

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
# db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Robot_resource, "/robot/<int:robot_id>")
# api.add_resource(UserList, '/users')
# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    from app.models import db

    db.init_app(app)
    app.run(port=5000, debug=True)
