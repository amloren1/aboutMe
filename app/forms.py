from flask_wtf import FlaskForm

# field types imported directly from wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, FloatField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    # first arg of each field is a descriptor or label
    # second is validator, optional. DataRequired makes sure that the field is filled
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class MessagesForm(FlaskForm):
    # first arg of each field is a descriptor or label
    # second is validator, optional. DataRequired makes sure that the field is filled
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    message = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class PlanetParamsForm(FlaskForm):
    # first arg of each field is a descriptor or label
    # second is validator, optional. DataRequired makes sure that the field is filled
    femg = FloatField('Fe/Mg', validators=[DataRequired()])
    simg = FloatField('Si/Mg', validators=[DataRequired()])
    mass = FloatField('Mass (M_earth)', validators=[DataRequired()])
    run = SubmitField('Run ExoPlex')


