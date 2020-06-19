from flask import Flask, render_template

from wtform_fields import *

app = Flask(__name__)
app.secret_key = 'secret-key'

@app.route("/",methods= ['GET','POST'])
def index():
    regitration_form = RegistrationForm
    return render_template("index.html",form = regitration_form)

if __name__ == '__main__':
    app.run(debug=True, port=2000)