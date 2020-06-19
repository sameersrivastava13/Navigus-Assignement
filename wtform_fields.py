from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    #The Registration form

    username = StringField('username_label')  #similar to label tag <label>
    password = PasswordField('password_label')
    confirm_pass = PasswordField('confirm_pass_label')

