from datetime import date


from flask_wtf import FlaskForm
# field types imported directly from wtf
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    PasswordField,
    StringField,
    SubmitField,
    TextField,
    TextAreaField,
    TimeField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """
        checks if username is already taken in the database in the case a user wants to change their username
        """
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Username taken, use a different one")

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


class RegistrationForm(FlaskForm):
    """
        allow users to register for extra permissions on the page
    """
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # custom validators below are automatically called by WTF
    #  using the standard convention of validate_<field_name> WTF knows to call these
    def validate_username(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Try another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered with an account.')

