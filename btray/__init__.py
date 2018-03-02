import os
import sys
import logging

from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PasswordType
from flask_sqlalchemy import orm

app = Flask(__name__, template_folder='../templates')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.secret_key = os.environ['SECRET_KEY']
app.config['ENVIRONMENT'] = os.environ['ENVIRONMENT']

login_manager = LoginManager()
login_manager.init_app(app)

if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.sqlite'


db = SQLAlchemy(app)
db.PasswordType = PasswordType
