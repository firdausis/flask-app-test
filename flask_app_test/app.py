from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/data_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ThisIsASecret'
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from . import models, resources

api.add_resource(resources.Login, '/api/dm/login')
