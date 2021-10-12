from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import db, Dino
from app.utils import check_grid, check_coords, check_position

dino_post_args = reqparse.RequestParser()

dino_post_args.add_argument(
    "x", type=int, help="x coord is required. [x: Integer, y: Integer]", required=True
)
dino_post_args.add_argument(
    "y", type=int, help="y coord is required. [x: Integer, y: Integer]", required=True
)

dino_get_args = reqparse.RequestParser()
dino_get_args.add_argument("id", type=int, help="ID is required", required=True)

dino_fields = {"id": fields.Integer, "x": fields.Integer, "y": fields.Integer}


class Dino_resource(Resource):
    @marshal_with(dino_fields)
    def get(self):
        args = dino_get_args.parse_args()
        result = Dino.query.filter_by(id=args["id"]).first()
        if not result:
            abort(404, message="Could not find dino with that id")
        return result

    @marshal_with(dino_fields)
    def post(self):
        args = dino_post_args.parse_args()

        check_grid()
        check_coords(args["x"], args["y"])
        check_position(args["x"], args["y"])

        ## check the space dim

        dino = Dino(x=args["x"], y=args["y"])

        db.session.add(dino)
        db.session.commit()

        return dino, 201
