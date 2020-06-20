from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    #The Registration form

    username = StringField("username_label",
                           validators=[InputRequired(message="Username Required"),
                                       Length(min=3, max=25, message="Username must be btw 3 and 25 characters")])

    password = PasswordField("Password_label", validators=[InputRequired(message="Password Required"),
                                                           Length(min=3, max=25,
                                                                  message="Password must be btw 3 and 25 characters")])
    confirm_pass = PasswordField("Confirm_Password_label", validators=[InputRequired(message="Password Required"),
                                                                       EqualTo('password',
                                                                               message="Passwords must match")])

    submit_button = SubmitField("Create")



