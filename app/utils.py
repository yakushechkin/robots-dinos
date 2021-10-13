"""
Helper funtions
"""

from itertools import cycle
from flask_restful import abort
from app.models import db, Dino, Robot, Game, Direction


def row2dict(row):

    """
    Converting a SQLAlchemy row to a python dict.
    The function borrowed from a function from
    https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    """

    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def check_position(x, y):

    """
    Check the occupancy of a position (x,y) in the grid.
    """
    robot_exist = Robot.query.filter_by(x=x, y=y).first()
    if robot_exist:
        abort(409, message=f"Oops! Robot (id {robot_exist.id})is already here ..")

    dino_exist = Dino.query.filter_by(x=x, y=y).first()
    if dino_exist:
        abort(409, message=f"Oops! Dinosaur (id {dino_exist.id}) is already here...")


def check_coords(x, y):

    """
    Check that the coordinates do not fall outside the grid.
    """

    grid_dim = db.session.query(Game).first()
    print(x, y, x >= grid_dim.dim or y >= grid_dim.dim)
    if x >= grid_dim.dim or y >= grid_dim.dim:
        abort(
            403,
            message="The coordinates lie outside the grid..."
            + f"(the grid is {grid_dim.dim}x{grid_dim.dim})",
        )


def check_grid():

    """
    Check the existence of a grid (game).
    """

    result = db.session.query(Game).first()
    if not result:
        abort(404, message="The grid doesn't exist. Please create a new space.")


def robot_action(robot, action):

    """
    The logic of the robot's actions.
    Options for action: 'move forward', 'move backward', 'turn left', 'turn right', 'attack'.
    """

    # create cycles to rotate the robot
    directions = [Direction.SOUTH, Direction.WEST, Direction.NORTH, Direction.EAST]
    directions_clockwise = cycle(directions)
    directions_counterclockwise = cycle(directions[::-1])

    message = {}

    if action == "attack":

        # looking for dinosaurs around
        dinosaurs = (
            db.session.query(Dino)
            .filter(Dino.x <= robot.x + 1)
            .filter(Dino.x >= robot.x - 1)
            .filter(Dino.y <= robot.y + 1)
            .filter(Dino.y >= robot.y - 1)
        )

        destroyed_dinos = 0
        destroyed_ids = []

        # kill dinosaurs
        for dinosaur in dinosaurs.all():
            destroyed_ids.append(dinosaur.id)
            db.session.query(Dino).filter(Dino.id == dinosaur.id).delete()
            destroyed_dinos += 1

        # update game table [n_destroyed_dinos, n_dinos]
        game = db.session.query(Game).first()
        game.n_destroyed_dinos += destroyed_dinos
        game.n_dinos -= destroyed_dinos
        db.session.commit()

        if destroyed_ids:
            message["message"] = (
                f"The robot {robot.id} destroyed {destroyed_dinos} "
                + f"dinosaurs (id(-s): {destroyed_ids}). {game.n_dinos} dinosaur(-s) left"
            )
        else:
            message[
                "message"
            ] = f"Not a single dinosaur was injured. {game.n_dinos} dinosaur(-s) left"

    elif action == "turn left":
        for direction in directions_counterclockwise:
            if robot.direction == direction:
                robot.direction = next(directions_counterclockwise)
                break

        message["message"] = f"The robot {robot.id} turned left"

    elif action == "turn right":
        print(robot.direction)
        for direction in directions_clockwise:
            if robot.direction == direction:
                robot.direction = next(directions_clockwise)
                break

        message["message"] = f"The robot {robot.id} turned right"

    elif action == "move forward":

        # creating temporary variables x and y for checking the occupancy of a position
        # and that the coordinates are inside the grid:
        if robot.direction == Direction.SOUTH:
            x, y = robot.x, robot.y - 1
        elif robot.direction == Direction.NORTH:
            x, y = robot.x, robot.y + 1
        elif robot.direction == Direction.EAST:
            x, y = robot.x + 1, robot.y
        elif robot.direction == Direction.WEST:
            x, y = robot.x - 1, robot.y

        check_position(x, y)
        check_coords(x, y)

        # update the robot record
        robot.x, robot.y = x, y

        message["message"] = f"The robot {robot.id} moved forward"

    elif action == "move backward":

        # creating temporary variables x and y for checking the occupancy of a position
        # and that the coordinates are inside the grid:
        if robot.direction == Direction.SOUTH:
            x, y = robot.x, robot.y + 1
        elif robot.direction == Direction.NORTH:
            x, y = robot.x, robot.y - 1
        elif robot.direction == Direction.EAST:
            x, y = robot.x - 1, robot.y
        elif robot.direction == Direction.WEST:
            x, y = robot.x + 1, robot.y

        check_position(x, y)
        check_coords(x, y)

        # update the robot record
        robot.x, robot.y = x, y

        message["message"] = f"The robot {robot.id} moved backward"

    return robot, message
