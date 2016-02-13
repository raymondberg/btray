from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PasswordType
from flask_sqlalchemy import orm

app = Flask(__name__, template_folder='../templates')

app.config.from_object('btray.configuration')
app.config.from_pyfile('../configuration.py')


login_manager = LoginManager()
login_manager.init_app(app)

if app.config['ENVIRONMENT'] == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
        app.config['MYSQL_USERNAME'],
        app.config['MYSQL_PASSWORD'],
        app.config['MYSQL_HOST'],
        app.config['MYSQL_PORT'],
        app.config['MYSQL_DATABASE']
    )
elif app.config['ENVIRONMENT'] == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.sqlite'


db = SQLAlchemy(app)
db.PasswordType = PasswordType
