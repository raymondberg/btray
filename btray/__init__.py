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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    app.config['MYSQL_USERNAME'],
    app.config['MYSQL_PASSWORD'],
    app.config['MYSQL_HOST'],
    app.config['MYSQL_PORT'],
    app.config['MYSQL_DATABASE']
)

db = SQLAlchemy(app)
db.PasswordType = PasswordType
