from datetime import date


from flask_wtf import FlaskForm
# field types imported directly from wtf
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextField,
    FloatField,
    DateField,
    TimeField
)
from wtforms.validators import DataRequired, Email, ValidationError

from app.models import User

class LoginForm(FlaskForm):
    # first arg of each field is a descriptor or label
    # second is validator, optional. DataRequired makes sure that the field is filled
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    #validation
    def validate_login(self, username, password):
        user = User.query.filter_by(username.data).first()

        if not user:
            raise ValidationError("Validation Message")
        elif user.password != password:
            raise ValidationError("Validation Message")

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



class CamQueryForm(FlaskForm):
    # first arg of each field is a descriptor or label
    # second is validator, optional. DataRequired makes sure that the field is filled
    start_date = DateField('Start date', validators=[DataRequired()])
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()], default=date.today())
    end_time = TimeField('End time', validators=[DataRequired()])
    find = SubmitField('Find')


