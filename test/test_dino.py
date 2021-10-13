from flask import Flask, json
from flask_restful import Api
import unittest
import requests
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


class TestDinos(unittest.TestCase):
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


    def create_robots(self):

        self.create_game()

        data = [
            {"x": 10, "y": 5, "direction": "EAST"},
            {"x": 2, "y": 18, "direction": "WEST"},
            {"x": 7, "y": 2, "direction": "EAST"},
            {"x": 14, "y": 38, "direction": "EAST"},
            {"x": 2, "y": 19, "direction": "EAST"},
        ]

        for i in range(len(data)):
                self.app.test_client().post("/robot/", data=data[i])

    def test_get_dino(self):

        self.create_game()

        dino_id = 1

        response = self.app.test_client().get(f"/dino/{dino_id}")
        data = json.loads(response.data)
        self.assertEqual(data["message"], f"Could not find dino with id {dino_id}")
        "Could not find dino with id 1"

        data = {"x": 10, "y": 5}
        self.app.test_client().post("/dino/", data=data)
        response = self.app.test_client().get(f"/dino/{dino_id}")
        resp_data = json.loads(response.data)
        self.assertEqual(
            resp_data, {"id": 1, "x": 10, "y": 5}
        )

    def test_invalid_create_dino(self):
        response = self.app.test_client().post("/dino/")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data["message"]["x"],
            "x coord is required. "
            + "[x: Integer, y: Integer]",
        )

    def test_create_dino_empty_space(self):

        data = {"x": 10, "y": 5}

        response = self.app.test_client().post("/dino/", data=data)
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            resp_data["message"], "The grid doesn't exist. Please create a new space."
        )

    def test_create_dino(self):

        self.create_game()

        data = [
            {"x": 10, "y": 5},
            {"x": 2, "y": 6},
            {"x": 7, "y": 2},
            {"x": 14, "y": 223},
            {"x": 2, "y": 6},
        ]

        response = self.app.test_client().post("dino/", data=data[0])
        self.assertEqual(response.status_code, 201)
        response = self.app.test_client().post("dino/", data=data[1])
        self.assertEqual(response.status_code, 201)
        response = self.app.test_client().post("dino/", data=data[2])
        resp_data = json.loads(response.data)
        self.assertEqual(
            resp_data, dict({"id": 3, "x": 7, "y": 2})
        )
        response = self.app.test_client().post("dino/", data=data[3])
        self.assertEqual(response.status_code, 405)
        response = self.app.test_client().post("dino/", data=data[4])
        self.assertEqual(response.status_code, 409)

    def test_create_dino_if_robot_occupies(self):

        self.create_robots()

        data = [
            {"x": 10, "y": 5},
            {"x": 2, "y": 6},
        ]

        response = self.app.test_client().post("/dino/", data=data[0])
        resp_data = json.loads(response.data)
        print(resp_data)
        self.assertEqual(
            resp_data["message"], "Oops! Robot (id 1) is already here..."
        )
        response = self.app.test_client().post("/dino/", data=data[1])
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
