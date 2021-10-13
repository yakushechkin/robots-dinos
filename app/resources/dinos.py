"""
Dinosaur Resource
"""

from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models.models import db, Dino, Game
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


class DinoResource(Resource):

    """
    Define HTTP methods (GET, POST) for the Dinosaurs.
    """

    @marshal_with(dino_fields)
    def get(self):

        """
        Get method retrieves the data about the current position.
        """

        check_grid()

        args = dino_get_args.parse_args()
        result = Dino.query.filter_by(id=args["id"]).first()
        if not result:
            abort(404, message=f"Could not find dino with id {args['id']}")
        return result, 200

    @marshal_with(dino_fields)
    def post(self):

        """
        POST method creates a new dinosaur.
        """

        args = dino_post_args.parse_args()

        # checks
        check_grid()
        check_coords(args["x"], args["y"])
        check_position(args["x"], args["y"])

        dino = Dino(x=args["x"], y=args["y"])

        # add a dino to the game table
        game = db.session.query(Game).first()
        game.n_dinos += 1

        db.session.add(dino)
        db.session.commit()

        return dino, 201
