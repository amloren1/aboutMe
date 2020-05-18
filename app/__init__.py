from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db) # database migration engine
# these lines let flask-login know where the login view is
login_manager = LoginManager(app)
login_manager.login_view = 'login' # login endpoint
login_manager.login_message_category = "info"

from app import routes, models #models will define the structure of the database