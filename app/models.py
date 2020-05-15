import datetime

from flask_login import UserMixin # used to meet requirements of flask-login
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

'''
    create a class for each database entity
    - db.Model is the base class inherited by Flask-SQLAlchemy
    - class variables define attributes of db entities
    - 
'''

# manage logged in users using flask-login
#  grab user from database using user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = True, default = 'user') # no duplicates allowed
    password_hash = db.Column(db.String(10), unique = True, nullable = True, default = 'None')

    def __repr__(self):
        # useful for printing details of the class instance
        return f"<User('{self.username}')>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140), nullable = True)
    name = db.Column(db.String(140), nullable = True)
    date = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Name: {self.name}\nmessage: {message}"

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    femg = db.Column(db.Float(), nullable = False, default = 1.0)
    simg = db.Column(db.Float(), nullable = False, default = 1.0)
    mass = db.Column(db.Float(), nullable = True)
    radius = db.Column(db.Float(), nullable = True)

    def __repr__(self):
        return f"<Fe/Mg: {self.femg}  SiMg: {self.simg}  Mass: {self.mass}  Radius: {self.radius}>"
