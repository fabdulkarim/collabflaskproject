import hashlib

from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc

from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required
from blueprints import internal_required

from datetime import datetime

from .model import Clients
from blueprints import db, app

from . import *

bp_client = Blueprint('client', __name__)
api = Api(bp_client)


class UserEdit(Resource):
    
    # clients = Clients()

    @jwt_required
    @internal_required    
    def put(self, id):
        policy = PasswordPolicy.from_names(
            length=6
            # uppercase=1,
            # numbers=1,
            # special=1,
            # nonletter=1
        )

        parser = reqparse.RequestParser()
        parser.add_argument('client_name', location='json', required=True)
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json', default=True)

        args = parser.parse_args()

        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        validation = policy.test(args['client_secret'])

        if validation == []:
            password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()

            qry.client_name = args['client_name'] ### INI JUGAK NDAK OLEH DIUBAH2
            qry.client_key = args['client_key'] ### JANGAN LUPA BAHWA KEY ITU UNIQUE
            qry.client_secret = password_digest
            qry.status = args['status']
            qry.updated_at = db.func.now()
            db.session.commit()

            return marshal(qry, Clients.response_fields), 200
        return {'status': 'failed', 'result': str(validation)}, 400, {'Content-Type': 'application/json'}
        
    @jwt_required
    @internal_required
    def delete(self, id):

        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.status = False
        qry.updated_at = db.func.now()
        db.session.commit()

        return {'message': 'deleted'}, 200

        # self.clients.delet(id)
        # return {'message': 'deleted'}, 200
        #pass

    @jwt_required
    @internal_required
    def post(self):


        ### key as username/code AB-XYZ (ab in alphabet), XYZ in numeric
        ### Standard input keyXX + secretXXX, both by id
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('client_name', location='args', required=True)
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        
        args = parser.parse_args()

        validation = policy.test(args['client_secret'])

        if validation == []:
            password_digest = hashlib.md5(args['client_secret'].encode()).hexdigest()
            
            client = Clients(args['client_name'], args['client_key'], password_digest)

            db.session.add(client)
            db.session.commit()

            app.logger.debug('DEBUG : %s', client)

            return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'failed', 'relust': str(validation)}, 400, {'Content-Type': 'application/json'}

class UserSignUp(Resource):

    def post(self):


        ### key as username/code AB-XYZ (ab in alphabet), XYZ in numeric
        ### Standard input keyXX + secretXXX, both by id
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        #parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            
            user = Users(args['username'], password_digest)

            db.session.add(user)
            db.session.commit()

            app.logger.debug('DEBUG : %s', user)

            return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'failed', 'result': str(validation)}, 400, {'Content-Type': 'application/json'}

api.add_resource(UserEdit, '/internal')
api.add_resource(UserSignUp, '/signup')