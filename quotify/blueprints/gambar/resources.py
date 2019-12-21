from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
#from sqlalchemy import desc
import os, random, string


from datetime import datetime


############# ADDING jwt + internal required for client, book, user
# from flask_jwt_extended import jwt_required
# from blueprints import internal_required

#from .model import Gambars
from blueprints import app # db

from . import *

####### adding image extractor to be saved in place ###############

from flask import Flask, request, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '../storage/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
###################################################################

bp_gambar = Blueprint('gambar', __name__)
api = Api(bp_gambar)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class GambarsResource(Resource):
    
    def post(self):
        if 'file' not in request.files:
            return {'message': 'gagal'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message': 'masih gagal'}, 401

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename2 = 'random'
            filename3 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32)) + '.jpg'
            file.save("%s/%s/%s" %(app.root_path, app.config['UPLOAD_FOLDER'],filename3)) #os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'message': 'success'} #url_for('uploaded_file', static=filename2)}
        #pass


api.add_resource(GambarsResource, '')