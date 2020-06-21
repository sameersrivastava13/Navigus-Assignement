import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
)
from wtform_fields import *
from models import *
from flask_socketio import SocketIO, send, join_room, leave_room
from time import localtime, strftime


# configure app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")


db = SQLAlchemy(app)

# Initializing Flask-socketIo
socket_app = SocketIO(app)

# list of documents available
documents = ["Python", "Java", "C++"]


# configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def index():
    registration_form = RegistrationForm()

    # updates the db if validation success
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data

        # password hashing for security
        hashed_pswd = pbkdf2_sha256.hash(
            password
        )  # take cares of both 16byte salt and iteartions (29000 by default)

        """To check username exists or not
                    Defined a function in wtform_fields.py file for this."""

        # Adding the user to the DATABASE
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        # flashing a message after successful registration
        flash("Registered Successfully! Now,Please login.", "success")
        return redirect(url_for("login"))

    return render_template("index.html", form=registration_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():  # it checks the post method and returns true
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for("chat"))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    """if not current_user.is_authenticated:
        flash("Please Login!","danger")
        return redirect(url_for("login"))"""
    return render_template("chat.html", username=current_user.username, rooms=documents)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("You have Logged out successfully!", "success")
    return redirect(url_for("login"))


@socket_app.on("message")
def message(data):

    print(f"\n\n{data}\n\n")

    send(
        {
            "msg": data["msg"],
            "username": data["username"],
            "timestamp": strftime("%b-%d %I:%M%p", localtime()),
        },
        room=data["room"],
    )
    # will sent data to all connected clients.will push data to a event bucket called message


@socket_app.on("join")
def join(data):
    room = data["room"]
    join_room(room)
    send(
        {
            "msg": data["username"]
            + " is currently viewing the "
            + data["room"]
            + " document."
        },
        room=data["room"],
    )


@socket_app.on("leave")
def leave(data):
    room = data["room"]
    leave_room(room)
    send(
        {"msg": data["username"] + " has left the " + data["room"] + " document."},
        room=data["room"],
    )


if __name__ == "__main__":
    app.run()  # socketio has its own run method


# after completion applied PEP-8 formatting.
