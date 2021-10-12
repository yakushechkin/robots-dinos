from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import db, Game
from app.utils import check_grid

game_post_args = reqparse.RequestParser()
game_post_args.add_argument(
    "dim", type=int, help="Set the dimension of the squere simulation space"
)

game_fields = {
    "dim": fields.Integer,
    "id": fields.Integer,
    "dim": fields.Integer,
    "n_robots": fields.Integer,
    "n_dinos": fields.Integer,
    "n_destroyed_dinos": fields.Integer,
}


class Game_resource(Resource):
    @marshal_with(game_fields)
    def get(self):

        check_grid()
        result = db.session.query(Game).first()

        return result, 200

    @marshal_with(game_fields)
    def post(self):
        args = game_post_args.parse_args()

        if db.session.query(Game).first():
            abort(409, message="The grid is already exist")

        if args:
            game = Game(dim=args["dim"])
        else:
            game = Game()

        db.session.add(game)
        db.session.commit()

        return game, 201
