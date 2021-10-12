from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import db, Robot
from app.utils import check_grid, check_coords, check_position

helper = "[x: Integer, y: Integer, direction: String [east,west,south or north]"

robot_put_args = reqparse.RequestParser()
robot_put_args.add_argument(
    "x",
    type=int,
    help="x coord is required. [x: Integer, y: Integer, direction: String [east,west,south or north]",
    required=True,
)
robot_put_args.add_argument(
    "y",
    type=int,
    help="y coord is required. [x: Integer, y: Integer, direction: String [east,west,south or north]",
    required=True,
)
robot_put_args.add_argument(
    "direction",
    type=str,
    help="Facing direction is required. [x: Integer, y: Integer, direction: String [east,west,south or north]".format(
        helper
    ),
    required=True,
)

robot_get_args = reqparse.RequestParser()
robot_get_args.add_argument("id", type=int, help="ID is required", required=True)


robot_fields = {
    "id": fields.Integer,
    "x": fields.Integer,
    "y": fields.Integer,
    "direction": fields.String,
}


class Robot_resource(Resource):
    @marshal_with(robot_fields)
    def get(self):
        args = robot_get_args.parse_args()
        result = Robot.query.filter_by(id=args["id"]).first()
        if not result:
            abort(404, message="Could not find robot with that id")
        return result

    @marshal_with(robot_fields)
    def post(self):
        args = robot_put_args.parse_args()

        check_grid()
        check_position(args["x"], args["y"])
        check_coords(args["x"], args["y"])

        robot = Robot(x=args["x"], y=args["y"], direction=args["direction"])

        db.session.add(robot)
        db.session.commit()

        return robot, 201
