from flask import Flask, json
from flask_restful import Api
import unittest
import os, sys, inspect

# change the current dir (to avoid using __init__.py and relative imports)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app.models import db
from config import Config
from app.resources.game import GameResource
from app.resources.robots import RobotResource, RobotGetResource
from app.resources.dinos import DinoResource, DinoGetResource


class TestGame(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config.from_object(Config)

        self.api.add_resource(RobotResource, "/robot/")
        self.api.add_resource(RobotGetResource, "/robot/<int:robot_id>")
        self.api.add_resource(DinoResource, "/dino/")
        self.api.add_resource(DinoGetResource, "/dino/<int:dino_id>")
        self.api.add_resource(GameResource, "/game/")

        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """

        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.app.config.from_object(Config)

        self.api.add_resource(RobotResource, "/robot/")
        self.api.add_resource(RobotGetResource, "/robot/<int:robot_id>")
        self.api.add_resource(DinoResource, "/dino/")
        self.api.add_resource(DinoGetResource, "/dino/<int:dino_id>")
        self.api.add_resource(GameResource, "/game/")

        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()

    def create_game(self):
        self.app.test_client().post("/game/")

    def create_dinos(self):

        self.create_game()

        data = [
            {"x": 10, "y": 5},
            {"x": 2, "y": 5},
            {"x": 1, "y": 7},
            {"x": 1, "y": 1},
            {"x": 2, "y": 1},
        ]
        for i in range(len(data)):
            self.app.test_client().post("/dino/", data=data[i])

    def create_robots(self):

        self.create_game()

        data = [
            {"x": 11, "y": 5, "direction": "EAST"},
            {"x": 2, "y": 18, "direction": "WEST"},
            {"x": 7, "y": 2, "direction": "EAST"},
            {"x": 14, "y": 14, "direction": "EAST"},
            {"x": 2, "y": 6, "direction": "EAST"},
        ]

        for i in range(len(data)):
            self.app.test_client().post("/robot/", data=data[i])

    def test_get_empty_game(self):
        response = self.app.test_client().get("/game/")
        data = json.loads(response.data)
        self.assertEqual(
            data["message"], "The grid doesn't exist. Please create a new space."
        )

    def test_create_game(self):
        response = self.app.test_client().post("/game/")
        self.assertEqual(response.status_code, 201)

    def test_game_already_created(self):
        response = self.app.test_client().post("/game/")
        self.assertEqual(response.status_code, 201)
        response = self.app.test_client().post("/game/")
        self.assertEqual(response.status_code, 409)

    def test_create_custom_dim_game(self):

        data = {"dim": 40}

        response = self.app.test_client().post("game/", data=data)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data["dim"], data["dim"])

        self.assertEqual(response.status_code, 201)
        response = self.app.test_client().get("game/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_dimension(self):

        data = {"dim": 0}

        response = self.app.test_client().post("game/", data=data)
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            resp_data["message"]["dim"],
            "Set the dimension of the square simulation space. Value must be >= 1",
        )

    def test_get_game(self):

        self.create_game()
        response = self.app.test_client().get("game/")
        resp_data = json.loads(response.data)
        self.assertEqual(
            resp_data,
            {
                "dim": 50,
                "id": 1,
                "n_robots": 0,
                "n_dinos": 0,
                "n_destroyed_dinos": 0,
                "robots": "[]",
                "dinosaurs": "[]",
            },
        )

        self.create_dinos()
        self.create_robots()
        response = self.app.test_client().get("game/")
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data["n_robots"], 5)
        self.assertEqual(resp_data["n_dinos"], 5)


if __name__ == "__main__":
    unittest.main()
