from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import Dino, db

dino_put_args = reqparse.RequestParser()
dino_put_args.add_argument("x", type=int, help="X coord is required", required=True)
dino_put_args.add_argument("y", type=int, help="Y coord is required", required=True)


dino_fields = {
	'id': fields.Integer,
	'x': fields.Integer,
	'y': fields.Integer
}

class Dino_resource(Resource):

    @marshal_with(dino_fields)
    def get(self, dino_id):
        result = Dino.query.filter_by(id=dino_id).first()
        if not result:
            abort(404, message="Could not find dino with that id")
        return result

    @marshal_with(dino_fields)
    def put(self, dino_id):
        args = dino_put_args.parse_args()
        result = Dino.query.filter_by(id=dino_id).first()
        if result:
            abort(409, message="Dino id taken...")
        
        dino = Dino(id=dino_id, x = args['x'], y=args['y'])

        db.session.add(dino)
        db.session.commit()
            
        return dino, 201
      