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


class TestRobots(unittest.TestCase):
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

    def test_get_robot(self):

        self.create_game()

        robot_id = 1

        response = self.app.test_client().get(f"/robot/{robot_id}")
        data = json.loads(response.data)
        self.assertEqual(data["message"], f"Could not find robot with id {robot_id}")
        "Could not find robot with id 1"

        data = {"x": 10, "y": 5, "direction": "EAST"}
        self.app.test_client().post("/robot/", data=data)
        response = self.app.test_client().get(f"/robot/{robot_id}")
        resp_data = json.loads(response.data)
        self.assertEqual(
            resp_data, {"id": 1, "x": 10, "y": 5, "direction": "Direction.EAST"}
        )

    def test_invalid_create_robot(self):
        response = self.app.test_client().post("/robot/")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data["message"]["x"],
            "x coord is required. "
            + "[x: Integer, y: Integer, direction: String [east,west,south or north]",
        )

    def test_create_robot_empty_space(self):

        data = {"x": 10, "y": 5, "direction": "EAST"}

        response = self.app.test_client().post("/robot/", data=data)
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            resp_data["message"], "The grid doesn't exist. Please create a new space."
        )

    def test_create_robot(self):

        self.create_game()

        data = [
            {"x": 10, "y": 5, "direction": "EAST"},
            {"x": 2, "y": 6, "direction": "WEST"},
            {"x": 7, "y": 2, "direction": "EAST"},
            {"x": 14, "y": 223, "direction": "EAST"},
            {"x": 2, "y": 6, "direction": "EAST"},
        ]

        response = self.app.test_client().post("robot/", data=data[0])
        self.assertEqual(response.status_code, 201)
        response = self.app.test_client().post("robot/", data=data[1])
        self.assertEqual(response.status_code, 201)
        response = self.app.test_client().post("robot/", data=data[2])
        resp_data = json.loads(response.data)
        self.assertEqual(
            resp_data, dict({"id": 3, "x": 7, "y": 2, "direction": "Direction.EAST"})
        )
        response = self.app.test_client().post("robot/", data=data[3])
        self.assertEqual(response.status_code, 405)
        response = self.app.test_client().post("robot/", data=data[4])
        self.assertEqual(response.status_code, 409)

    def test_create_robot_if_dino_occupies(self):

        self.create_dinos()

        data = [
            {"x": 10, "y": 5, "direction": "EAST"},
            {"x": 2, "y": 6, "direction": "WEST"},
        ]

        response = self.app.test_client().post("/robot/", data=data[0])
        resp_data = json.loads(response.data)
        self.assertEqual(
            resp_data["message"], "Oops! Dinosaur (id 1) is already here..."
        )
        response = self.app.test_client().post("/robot/", data=data[1])
        self.assertEqual(response.status_code, 201)

    def test_move_forward(self):

        data = [
            {"x": 1, "y": 6, "direction": "WEST"},
            {"x": 0, "y": 0, "direction": "EAST"},
            {"x": 3, "y": 6, "direction": "SOUTH"},
            {"x": 3, "y": 6, "direction": "NORTH"},
            {"x": 3, "y": 49, "direction": "NORTH"},
            {"x": 0, "y": 49, "direction": "WEST"},
            {"x": 1, "y": 7, "direction": "SOUTH"},
        ]

        data_action = [
            {"id": 1, "action": "move forward"},
            {"id": 2, "action": "move forward"},
            {"id": 3, "action": "move forward"},
            {"id": 4, "action": "move forward"},
            {"id": 5, "action": "move forward"},
            {"id": 6, "action": "move forward"},
            {"id": 7, "action": "move forward"},
        ]

        self.create_game()

        # 'WEST'
        response = self.app.test_client().post("/robot/", data=data[0])
        response = self.app.test_client().put("/robot/", data=data_action[0])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [0, 6])

        # 'EAST'
        response = self.app.test_client().post("/robot/", data=data[1])
        response = self.app.test_client().put("/robot/", data=data_action[1])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [1, 0])

        # 'SOUTH'
        response = self.app.test_client().post("/robot/", data=data[2])
        response = self.app.test_client().put("/robot/", data=data_action[2])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [3, 5])

        # 'NORTH' create the robot in he place that was occupied by another robot
        response = self.app.test_client().post("/robot/", data=data[3])
        response = self.app.test_client().put("/robot/", data=data_action[3])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [3, 7])

        # 'NORTH' move outside of the grid y > dim
        response = self.app.test_client().post("/robot/", data=data[4])
        response = self.app.test_client().put("/robot/", data=data_action[4])
        self.assertEqual(response.status_code, 405)

        # 'WEST' move outside of the grid x < 0
        response = self.app.test_client().post("/robot/", data=data[5])
        response = self.app.test_client().put("/robot/", data=data_action[5])
        self.assertEqual(response.status_code, 405)

        # 'SOUTH' move to the place that is occupied by the robot
        response = self.app.test_client().post("/robot/", data=data[6])
        response = self.app.test_client().put("/robot/", data=data_action[6])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [1, 6])

    def test_move_backward(self):

        data = [
            {"x": 1, "y": 6, "direction": "EAST"},
            {"x": 0, "y": 0, "direction": "WEST"},
            {"x": 3, "y": 6, "direction": "NORTH"},
            {"x": 3, "y": 6, "direction": "SOUTH"},
            {"x": 3, "y": 49, "direction": "SOUTH"},
            {"x": 0, "y": 49, "direction": "EAST"},
            {"x": 1, "y": 7, "direction": "NORTH"},
        ]

        data_action = [
            {"id": 1, "action": "move backward"},
            {"id": 2, "action": "move backward"},
            {"id": 3, "action": "move backward"},
            {"id": 4, "action": "move backward"},
            {"id": 5, "action": "move backward"},
            {"id": 6, "action": "move backward"},
            {"id": 7, "action": "move backward"},
        ]

        self.create_game()

        # 'EAST'
        response = self.app.test_client().post("/robot/", data=data[0])
        response = self.app.test_client().put("/robot/", data=data_action[0])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [0, 6])

        # 'WEST'
        response = self.app.test_client().post("/robot/", data=data[1])
        response = self.app.test_client().put("/robot/", data=data_action[1])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [1, 0])

        # 'NORTH'
        response = self.app.test_client().post("/robot/", data=data[2])
        response = self.app.test_client().put("/robot/", data=data_action[2])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [3, 5])

        # 'SOUTH' create the robot in he place that was occupied by another robot
        response = self.app.test_client().post("/robot/", data=data[3])
        response = self.app.test_client().put("/robot/", data=data_action[3])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [3, 7])

        # 'SOUTH' move outside of the grid y > dim
        response = self.app.test_client().post("/robot/", data=data[4])
        response = self.app.test_client().put("/robot/", data=data_action[4])
        self.assertEqual(response.status_code, 405)

        # 'EAST' move outside of the grid x < 0
        response = self.app.test_client().post("/robot/", data=data[5])
        response = self.app.test_client().put("/robot/", data=data_action[5])
        self.assertEqual(response.status_code, 405)

        # 'NORTH' move to the place that is occupied by the robot
        response = self.app.test_client().post("/robot/", data=data[6])
        response = self.app.test_client().put("/robot/", data=data_action[6])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([resp_data["x"], resp_data["y"]], [1, 6])

    def test_turn_left(self):

        data = [
            {"x": 1, "y": 6, "direction": "EAST"},
            {"x": 0, "y": 0, "direction": "WEST"},
            {"x": 3, "y": 6, "direction": "NORTH"},
            {"x": 2, "y": 6, "direction": "SOUTH"},
        ]

        data_action = [
            {"id": 1, "action": "turn left"},
            {"id": 2, "action": "turn left"},
            {"id": 3, "action": "turn left"},
            {"id": 4, "action": "turn left"},
        ]

        self.create_game()

        # 'EAST'
        response = self.app.test_client().post("/robot/", data=data[0])
        response = self.app.test_client().put("/robot/", data=data_action[0])
        response = self.app.test_client().get("/robot/1")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.NORTH")

        # 'WEST'
        response = self.app.test_client().post("/robot/", data=data[1])
        response = self.app.test_client().put("/robot/", data=data_action[1])
        response = self.app.test_client().get("/robot/2")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.SOUTH")

        # 'NORTH'
        response = self.app.test_client().post("/robot/", data=data[2])
        response = self.app.test_client().put("/robot/", data=data_action[2])
        response = self.app.test_client().get("/robot/3")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.WEST")

        # 'SOUTH'
        response = self.app.test_client().post("/robot/", data=data[3])
        response = self.app.test_client().put("/robot/", data=data_action[3])
        response = self.app.test_client().get("/robot/4")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.EAST")

    def test_turn_right(self):

        data = [
            {"x": 1, "y": 6, "direction": "NORTH"},
            {"x": 0, "y": 0, "direction": "SOUTH"},
            {"x": 3, "y": 6, "direction": "WEST"},
            {"x": 2, "y": 6, "direction": "EAST"},
        ]

        data_action = [
            {"id": 1, "action": "turn right"},
            {"id": 2, "action": "turn right"},
            {"id": 3, "action": "turn right"},
            {"id": 4, "action": "turn right"},
        ]

        self.create_game()

        # 'EAST'
        response = self.app.test_client().post("/robot/", data=data[0])
        response = self.app.test_client().put("/robot/", data=data_action[0])
        response = self.app.test_client().get("/robot/1")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.EAST")

        # 'WEST'
        response = self.app.test_client().post("/robot/", data=data[1])
        response = self.app.test_client().put("/robot/", data=data_action[1])
        response = self.app.test_client().get("/robot/2")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.WEST")

        # 'NORTH'
        response = self.app.test_client().post("/robot/", data=data[2])
        response = self.app.test_client().put("/robot/", data=data_action[2])
        response = self.app.test_client().get("/robot/3")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.NORTH")

        # 'SOUTH'
        response = self.app.test_client().post("/robot/", data=data[3])
        response = self.app.test_client().put("/robot/", data=data_action[3])
        response = self.app.test_client().get("/robot/4")
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["direction"], "Direction.SOUTH")

    def test_attack(self):

        data = [
            {"x": 1, "y": 2, "direction": "NORTH"},
            {"x": 15, "y": 15, "direction": "SOUTH"},
        ]

        data_action = [{"id": 1, "action": "attack"}, {"id": 2, "action": "attack"}]

        self.create_game()

        # create dinos:
        #     {"x": 10, "y": 5},
        #     {"x": 2, "y": 5},
        #     {"x": 1, "y": 7},
        #     {"x": 1, "y": 1},
        #     {"x": 2, "y": 1}

        self.create_dinos()

        # 2 dinosaurs around
        response = self.app.test_client().post("/robot/", data=data[0])
        response = self.app.test_client().put("/robot/", data=data_action[0])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            resp_data["message"],
            "The robot 1 destroyed 2 dinosaurs (id(-s): [4, 5]). 3 dinosaur(-s) left",
        )

        # 0 dinosaurs around
        response = self.app.test_client().post("/robot/", data=data[1])
        response = self.app.test_client().put("/robot/", data=data_action[1])
        resp_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            resp_data["message"],
            "Not a single dinosaur was injured. 3 dinosaur(-s) left",
        )


if __name__ == "__main__":
    unittest.main()
