from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256


class RegistrationForm(FlaskForm):
    #The Registration form

    username = StringField("username_label",
                           validators=[InputRequired(message="Username Required"),
                                       Length(min=3, max=25, message="Username must be btw 3 and 25 characters")])

    password = PasswordField("Password_label", validators=[InputRequired(message="Password Required"),
                                                           Length(min=3, max=25,message="Password must be btw 3 and 25 characters")])
    confirm_pass = PasswordField("Confirm_Password_label", validators=[InputRequired(message="Password Required"),
                                                                       EqualTo('password',message="Passwords must match")])

    submit_button = SubmitField("Create")

    def validate_username(self,username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Please try another username, this username already exits!.")


def invalid_credentials(form,field):
    #Username and password checker
    username = form.username.data
    password_entered = field.data

    #check credantials is valid
    user_object = User.query.filter_by(username=username).first()   #if does not exist return none
    if user_object is None:
        raise ValidationError("Username or password is incorrect")

    elif not pbkdf2_sha256.verify(password_entered,user_object.password):
        raise ValidationError("Username or password is incorrect")

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('username_label',validators=[InputRequired(message="Username required.")])
    password = PasswordField("password_label",validators=[InputRequired(message="Password Required."),invalid_credentials])

    submit_button = SubmitField("Login")




