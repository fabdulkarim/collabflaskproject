from flask import Flask , request
import json,logging
from logging.handlers import RotatingFileHandler
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os 

import json
from datetime import timedelta
from functools import wraps
from flask import Flask, request 
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

app= Flask(__name__)

from blueprints.timpa.resources import bp_merge

app.register_blueprint(bp_merge, url_prefix="/merge")

@app.after_request

def after_request(response):
    if response.status_code==200:
        try:
            requestData=request.get_json()
        except Exception as e:
            requestData= request.args.to_dict()
        app.logger.info("REQUEST_LOG\t%s",
            json.dumps({ 
            'status_code': response.status_code,
            'method' :request.method,
            'code':response.status, 
            'uri':request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        try:
            requestData=request.get_json()
        except Exception as e:
            requestData= request.args.to_dict()
        app.logger.warning("REQUEST_LOG\t%s",
            json.dumps({ 
            'status_code': response.status_code,
            'method' :request.method,
            'code':response.status, 
            'uri':request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response