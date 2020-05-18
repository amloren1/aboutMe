from datetime import datetime

from flask_login import UserMixin # used to meet requirements of flask-login
from hashlib import md5
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
    email = db.Column(db.String(120), index=True, unique=True, default = 'none@none.com')
    password_hash = db.Column(db.String(10), unique = True, nullable = True, default = 'None')
    about_me = db.Column(db.String(140)) # 140 character about me
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        # useful for printing details of the class instance
        return f"<User('{self.username}')>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        function to pull avatars from Gravatar website. takes hashed email and image size as arguments
        """
        email = (self.email if self.email else 'defaul@default.com')
        digest = md5(email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140), nullable = True)
    name = db.Column(db.String(140), nullable = True)
    date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

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
