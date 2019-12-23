from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
#from sqlalchemy import desc
import os, random, string


from datetime import datetime

from .image_filtering_resource import download_file, filterImage
from .scriptFadhil import fadhilProcess
#import scriptFadhil
from .scriptWoka import MergeResource


############# ADDING jwt + internal required for client, book, user
from flask_jwt_extended import jwt_required
from blueprints import internal_required, non_internal_required

#from .model import Gambars
from blueprints import app, db

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

    @jwt_required
    @non_internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('arg1', location='args')
        parser.add_argument('arg2', location='args')
        parser.add_argument('arg3', location='args')
        parser.add_argument('arg4', location='args')
        
        args = parser.parse_args()

        if len(args) < 4:
            return {'message':'argumen tidak lengkap'}, 404

        if 'file' not in request.files:
            return {'message': 'gagal'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message': 'masih gagal'}, 401

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename2 = 'random'
            filename3 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8)) + '.jpg'
            file.save(os.path.abspath(filename3))
            #file.save("%s/%s/%s" %(app.root_path, app.config['UPLOAD_FOLDER'],filename3))            
            #absolute_path = "%s/%s/%s" %(app.root_path, app.config['UPLOAD_FOLDER'],filename3)
            #os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return {'message': 'success'} #url_for('uploaded_file', static=filename2)}
        #pass
            temp_abs_path = os.path.abspath(filename3)
            ## hash upload ##
            # urlAwal = MergeResource.uploads(temp_abs_path)
            #print(urlAwal)



            ## subpro fadhil ##
            # a,b = fadhilProcess(absolute_path,args['arg1'],args['arg2'])
            a,b = fadhilProcess(temp_abs_path,args['arg1'],args['arg2'])
            #a,b = fadhilProcess(temp_abs_path,args['arg1'],args['arg2'])
            ##
            #trial nyoba upload after resize
            urlAwal = MergeResource.uploads(temp_abs_path)
            #dict_ref = {'text':a,'author':b}
            ## subpro mas bimon ##
            try:
                fileBimon = filterImage(download_file(urlAwal)) 
                urlBimon = MergeResource.uploads(fileBimon)
                terakhir = MergeResource.merge(urlBimon,a,b)            
            except:
                #print(urlBimon)
                terakhir = MergeResource.merge(urlAwal,a,b)
            
            urlFinal = MergeResource.uploads('mantap.jpg')
            final = os.path.abspath('mantap.jpg')


            ## mas woka time 
            

            return {'status':'success', 'url_to_see':urlFinal}, 200

api.add_resource(GambarsResource, '')