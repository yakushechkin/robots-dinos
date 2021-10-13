"""
Game(grid) Resource
"""

from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import db, Game, Robot, Dino
from app.utils import check_grid, row2dict

game_post_args = reqparse.RequestParser()
game_post_args.add_argument(
    "dim", type=int, help="Set the dimension of the square simulation space"
)

game_fields = {
    "dim": fields.Integer,
    "id": fields.Integer,
    "n_robots": fields.Integer,
    "n_dinos": fields.Integer,
    "n_destroyed_dinos": fields.Integer,
    "robots": fields.String,
    "dinosaurs": fields.String,
}


class GameResource(Resource):

    """
    Define HTTP methods (GET, POST) for the Game.
    """

    @marshal_with(game_fields)
    def get(self):

        """
        Get method retrieves the data about the current game.
        """

        check_grid()

        result = db.session.query(Game).first()

        robots = db.session.query(Robot).all()
        dinos = db.session.query(Dino).all()

        robots_info, dinos_info = [], []

        for rob in robots:
            robots_info.append(
                {"id": rob.id, "x": rob.x, "y": rob.y, "direction": rob.direction}
            )
        for din in dinos:
            dinos_info.append({"id": din.id, "x": din.x, "y": din.y})

        robots, dinos = str(robots_info), str(dinos_info)

        result = row2dict(result)
        result["robots"] = robots
        result["dinosaurs"] = dinos

        return result, 200

    @marshal_with(game_fields)
    def post(self):

        """
        POST method sends data to the server and creates a new game.
        """
        args = game_post_args.parse_args()

        if db.session.query(Game).first():
            abort(409, message="The grid already exists")

        if args:
            game = Game(dim=args["dim"])
        else:
            game = Game()

        db.session.add(game)
        db.session.commit()

        return game, 201
