from flask import Flask, render_template

from wtform_fields import *
from models import *


app = Flask(__name__)
app.secret_key = 'secret-key'

#COnfigure database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://czcphntronkggv:62a44072340aa811d5918d6e7af96cc4dc7a6c4d259544291307ff0181ac5719@ec2-18-235-20-228.compute-1.amazonaws.com:5432/db4nggt73in7ap"

db = SQLAlchemy(app)


@app.route("/",methods= ['GET','POST'])
def index():
    regitration_form = RegistrationForm()

    if regitration_form.validate_on_submit():
        username = regitration_form.username.data
        password = regitration_form.password.data

        #check username exists or not
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username!"

        #Adding the user to the DATABASE
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted"

    return render_template("index.html",form = regitration_form)

if __name__ == '__main__':
    app.run(debug=True, port=2000)