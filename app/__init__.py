import logging
from logging.handlers import RotatingFileHandler
import os

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

if not app.debug:
    if not os.path.exists("logs"):
            os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/aboutME.log", maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('aboutMe startup')

from app import routes, models, errors #models will define the structure of the database