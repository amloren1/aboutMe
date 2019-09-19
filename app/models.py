import datetime

from flask_login import UserMixin

from app import db, login_manager


# manage logged in users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(10), unique = True, nullable = False)

    def __repr__(self):
        return f"<User('{self.username}')>"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140), nullable = False)
    name = db.Column(db.String(140), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Name: {self.name}\nmessage: {message}"

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    femg = db.Column(db.Float(), nullable = False)
    simg = db.Column(db.Float(), nullable = False)
    mass = db.Column(db.Float(), nullable = True)
    radius = db.Column(db.Float(), nullable = True)

    def __repr__(self):
        return f"<Fe/Mg: {self.femg}  SiMg: {self.simg}  Mass: {self.mass}  Radius: {self.radius}>"
