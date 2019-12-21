import hashlib

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..user.model import Users

bp_login = Blueprint('login', __name__)
api = Api(bp_login)

## HARD COPY FROM PREV, needs modification

## requirement pertama: nambahin client_id di claims karena akan dipakai
## oleh user penerbit()

## modifikasi di bagian jwt_fields, dijepret ke claims, apa perlu buat sistem /client?
class CreateTokenResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()

        if args['client_key'] == 'admin' and args['client_secret'] == 'admin':
            token = create_access_token(identity=args['client_key'], user_claims={'isadmin':True})
            return {'token': token}, 200

        password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()

        qry = Clients.query.filter_by(client_key=args['client_key']).filter_by(client_secret=password_digest)

        clientData = qry.first()

        if clientData is not None:
            clientData = marshal(clientData, Clients.jwt_claims_fields) 
            clientData['isadmin'] = False
            
            token = create_access_token(identity=args['client_key'], user_claims=clientData)        
            
            return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return claims, 200



api.add_resource(CreateTokenResource, '')