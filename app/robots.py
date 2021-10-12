from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from app.models import Robot, db

robot_put_args = reqparse.RequestParser()
robot_put_args.add_argument("x", type=int, help="X coord is required", required=True)
robot_put_args.add_argument("y", type=int, help="Y coord is required", required=True)
robot_put_args.add_argument("direction", type=str, help="Facing direction is required", required=True)


robot_fields = {
	'id': fields.Integer,
	'x': fields.Integer,
	'y': fields.Integer,
	'direction': fields.String
}

class Robot_resource(Resource):

    @marshal_with(robot_fields)
    def get(self, robot_id):
        result = Robot.query.filter_by(id=robot_id).first()
        if not result:
            abort(404, message="Could not find robot with that id")
        return result

    @marshal_with(robot_fields)
    def put(self, robot_id):
        args = robot_put_args.parse_args()
        result = Robot.query.filter_by(id=robot_id).first()
        if result:
            abort(409, message="Robot id taken...")
        
        robot = Robot(id=robot_id, x = args['x'], y=args['y'], direction=args['direction'])

        db.session.add(robot)
        db.session.commit()
            
        return robot, 201
      