import json
import os
from datetime import timedelta
from functools import wraps

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

from flask_script import Manager


app = Flask(__name__) # this is yang menyebabkan lokasi app.rootnya disini


app.config['JWT_SECRET_KEY'] = '1Y1uHnISqEZ6MNlH03Jh0plYzz6gCUq1'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims= get_jwt_claims()
        if not claims['isadmin']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def non_internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims= get_jwt_claims()
        if claims['isadmin']:
            return {'status': 'FORBIDDEN', 'message': 'Not meant for Admins'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


# #################### NAMBAHIN BUAT TESTING
# try:
#     env = os.environ.get('FLASK_ENV', 'development') #nama, default
#     if env == 'testing':
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:JalanTidarno.23@localhost:3306/restDB_test'
#     else:
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:JalanTidarno.23@localhost:3306/restDB'
# except Exception as e:
#     raise e

##### HARUS DI ATAS ######################################################

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:JalanTidarno.23@localhost:3306/flaskproDB' #connectionstring
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


######### THIS IS CALLED MIDDLEWARE ##################
######################################################
############## seluruh si bagian dengan ##############
##### dengan decorator dan kawan-kawan ###############

@app.after_request
def after_request(response):
    
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({ 
            'status_code': response.status_code, # ini ngebuat 400 gak bisa masuk 
            'request': requestData, 'response': json.loads(response.data.decode('utf-8'))}))
    else:
        app.logger.error("REQUEST_LOG\t%s", json.dumps({ 
            'status_code': response.status_code, # ini ngebuat 400 gak bisa masuk 
            'request': requestData, 'response': json.loads(response.data.decode('utf-8'))}))

    # ini sesuai yang masnya, jadi ngambil argumennya, tadi error get_json
    # dipisah jadi info dan error
    return response

from blueprints.gambar.resources import bp_gambar
app.register_blueprint(bp_gambar, url_prefix='/gambar')

from blueprints.user.resources import bp_user
app.register_blueprint(bp_user, url_prefix='')

from blueprints.login import bp_login
app.register_blueprint(bp_login, url_prefix='/login')

db.create_all()