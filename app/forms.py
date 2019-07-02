from flask_wtf import FlaskForm

# field types imported directly from wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # first arg of each field is a descriptor or label
    # second is validator, optional. DataRequired makes sure that the field is filled
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')