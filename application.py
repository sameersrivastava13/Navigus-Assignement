from flask import Flask, render_template, redirect, url_for,flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtform_fields import *
from models import *
from flask_socketio import SocketIO,send,emit,join_room,leave_room
from time import localtime,strftime



app = Flask(__name__)
app.secret_key = 'secret-key'

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://czcphntronkggv:62a44072340aa811d5918d6e7af96cc4dc7a6c4d259544291307ff0181ac5719@ec2-18-235-20-228.compute-1.amazonaws.com:5432/db4nggt73in7ap"

db = SQLAlchemy(app)

#configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route("/",methods= ['GET','POST'])
def index():
    regitration_form = RegistrationForm()

    if regitration_form.validate_on_submit():
        username = regitration_form.username.data
        password = regitration_form.password.data

        #password hashing for security
        hashed_pswd = pbkdf2_sha256.hash(password)  # take cares of both 16byte salt and iteartions (29000 iterations by default )

        """To check username exists or not
            Defined a function in wtform_fields.py file for this."""

        #Adding the user to the DATABASE
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        # Flashing a message here
        flash("Registered Successfully! Now,Please login.", "success")
        return redirect(url_for('login'))

    return render_template("index.html",form = regitration_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():  # it checks the post method and returns true
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    return render_template("login.html", form=login_form)




@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please Login!"
    return "chat with me"
    """flash("Please Login!","danger")
    return redirect(url_for("login"))"""
    #return render_template('write.html', username=current_user.username,rooms=ROOMS)

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    #flash("You have Logged out successfully!","success")
    return redirect(url_for("login"))

"""@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    send({'msg': data['username']  + " has joined the " + data['room'] + " room."},room=data['room'])

@socketio.on('leave')
def leave(data):
    room = data['room']
    leave_room(room)
    send({'msg': data['username'] + " has left the" + data['room'] + " room."},room=data['room'])
"""




"""@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")

    send({'msg': data['msg'],'username': data['username'],'timestamp': strftime('%b-%d %I:%M%p',localtime())},room=data['room'])
    #will sent data to all connected clients.will push data to a event bucket called message
"""

if __name__ == '__main__':
    app.run(debug=True, port=2000)