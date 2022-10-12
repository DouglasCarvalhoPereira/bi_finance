from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask_login import LoginManager


app = Flask(__name__)

#Token Forms
app.config['SECRET_KEY'] = '4c6b928bf755c7d7d21e321900133925'

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nork_town.db'
db = SQLAlchemy(app)

#App Bycrypt
bycrypt = Bcrypt(app)

#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar essa página!'
login_manager.login_message_category = 'alert-info'

from nork_town import routes