import hashlib

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..user.model import Users

bp_login = Blueprint('login', __name__)
api = Api(bp_login)

## HARD COPY FROM PREV, needs modification

class CreateTokenResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        if args['username'] == 'admin' and args['password'] == 'admin':
            token = create_access_token(identity=args['username'], user_claims={'isadmin':True})
            return {'token': token}, 200

        password_digest = hashlib.md5(args['password'].encode()).hexdigest()

        qry = Users.query.filter_by(username=args['username']).filter_by(password=password_digest)

        clientData = qry.first()

        if clientData is not None:
            clientData = marshal(clientData, Users.jwt_claims_fields) 
            clientData['isadmin'] = False
            
            token = create_access_token(identity=args['username'], user_claims=clientData)        
            
            return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return claims, 200



api.add_resource(CreateTokenResource, '')