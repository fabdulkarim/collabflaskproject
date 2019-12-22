from blueprints import db
from flask_restful import fields, inputs

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #client_name = db.Column(db.String(255), nullable=False) #agar dapat dibedakan per entry
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    #status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'created_at': fields.String,
        'updated_at': fields.String
    }


    #penambahan client_id supaya isa di akses nanti pas melakukan seleksi
    ## BIAR RA USAH QUERY BALIK PAKEK clid + clna LANGSUNG AE LAH
    ## WIS MALES AKU
    jwt_claims_fields = {
        'id' : fields.Integer,
        'username': fields.String,
    }

    def __init__(self, username, password): 
        #self.client_id = client_id autogenerate
        self.username = username 
        self.password = password

    def __repr__(self):
        return '<Client %r %s>' % (self.id, self.username)