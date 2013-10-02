from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

manager = flask.ext.restless.APIManager(app,  flask_sqlalchemy_db=db)

from myapp.views import aview
from myapp.models import User

manager.create_api(User, methods=['GET', 'POST', 'DELETE'])