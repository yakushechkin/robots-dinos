from flask import Flask
from flask_restful import Api

from config import Config

# import resources
from app.resources.game import GameResource
from app.resources.robots import RobotResource
from app.resources.dinos import DinoResource

# uncomment if you want DB to be refreshed each run (1/2)
# from app.models import Dino, Robot, Game


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)


@app.before_first_request
def create_tables():
    db.create_all()


# uncomment if you want DB to be refreshed each run (2/2)
# clear tables
# try:
#     db.session.query(Dino).delete()
#     db.session.query(Robot).delete()
#     db.session.query(Game).delete()
#     db.session.commit()
# except:
#     db.session.rollback()


api.add_resource(RobotResource, "/robot/")
api.add_resource(DinoResource, "/dino/")
api.add_resource(GameResource, "/game/")


if __name__ == "__main__":
    from app.models import db

    db.init_app(app)
    app.run(port=5000, debug=True)
