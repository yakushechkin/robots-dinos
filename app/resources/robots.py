"""
Robot Resource
"""

from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models.models import db, Robot, Game
from app.utils import row2dict, check_grid, check_coords, check_position, robot_action

robot_get_args = reqparse.RequestParser()
robot_get_args.add_argument("id", type=int, help="Please specify the robot id")

robot_post_args = reqparse.RequestParser()
robot_post_args.add_argument(
    "x",
    type=int,
    help="x coord is required. [x: Integer, y: Integer,"
    + " direction: String [east,west,south or north]",
    required=True,
)
robot_post_args.add_argument(
    "y",
    type=int,
    help="y coord is required. [x: Integer, y: Integer,"
    + " direction: String [east,west,south or north]",
    required=True,
)
robot_post_args.add_argument(
    "direction",
    type=str,
    help="Facing direction is required. [x: Integer, y: Integer,"
    + " direction: String [east,west,south or north]",
    required=True,
)

robot_put_args = reqparse.RequestParser()
robot_put_args.add_argument(
    "id",
    type=int,
    help="The robot id is required. [id: Integer, action: 'move forward',"
    + " 'move backward', 'turn left', 'turn right', 'attack']",
    required=True,
)
robot_put_args.add_argument(
    "action",
    type=str,
    help="Action is required. Actions: 'move forward', 'move backward', "
    + "'turn left', 'turn right', 'attack'",
    choices=["move forward", "move backward", "turn left", "turn right", "attack"],
    required=True,
)

robot_fields = {
    "id": fields.Integer,
    "x": fields.Integer,
    "y": fields.Integer,
    "direction": fields.String,
}

robot_put_fields = {
    "message": fields.String,
    "id": fields.Integer,
    "x": fields.Integer,
    "y": fields.Integer,
    "direction": fields.String,
}


class RobotResource(Resource):

    """
    Define HTTP methods (GET, POST, PUT) for the Robot.
    """

    @marshal_with(robot_fields)
    def get(self):

        """
        Get method retrieves the data about the position, direction.
        """

        check_grid()

        args = robot_get_args.parse_args()
        result = Robot.query.filter_by(id=args["id"]).first()
        if not result:
            abort(404, message=f"Could not find robot with id {args['id']}")
        return result, 200

    @marshal_with(robot_fields)
    def post(self):

        """
        POST method creates a new robot.
        """

        args = robot_post_args.parse_args()

        check_grid()
        check_position(args["x"], args["y"])
        check_coords(args["x"], args["y"])

        robot = Robot(x=args["x"], y=args["y"], direction=args["direction"])

        # add a robot to the game table
        game = db.session.query(Game).first()
        game.n_robots += 1

        db.session.add(robot)
        db.session.commit()

        return robot, 201

    @marshal_with(robot_put_fields)
    def put(self):

        """
        PUT method performs the robot action and
        updates the existing location or direction of the robot.
        """

        args = robot_put_args.parse_args()

        check_grid()

        robot = Robot.query.filter_by(id=args["id"]).first()
        if not robot:
            abort(404, message=f"Could not find robot with id {args['id']}")

        robot, message = robot_action(robot, args["action"])

        db.session.commit()

        robot_dict = row2dict(robot)
        message.update(robot_dict)

        return message, 200
