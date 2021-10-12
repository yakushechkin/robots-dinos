from flask_restful import abort
from app.models import db, Dino, Robot, Game


def check_position(x, y):
    robot_exist = Robot.query.filter_by(x=x, y=y).first()
    if robot_exist:
        abort(409, message="Ops, Robot is already here ..")

    dino_exist = Dino.query.filter_by(x=x, y=y).first()
    if dino_exist:
        abort(409, message="Ops, Dinosaur is already here...")


def check_coords(x, y):
    grid_dim = db.session.query(Game).first()
    print(x, y, x >= grid_dim.dim or y >= grid_dim.dim)
    if x >= grid_dim.dim or y >= grid_dim.dim:
        abort(
            403,
            message="The coordinates lie outside the grid... (the grid is {}x{})".format(
                grid_dim.dim, grid_dim.dim
            ),
        )


def check_grid():
    result = db.session.query(Game).first()
    if not result:
        abort(
            404,
            message="The grid doesn't exist. Please create a space. .../game/ POST ",
        )
