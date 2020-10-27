from datetime import time
import os

from flask import Flask, request, render_template
from models import RegForm, LoginForm
from flask_bootstrap import Bootstrap
import hashlib
import datetime

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = hashlib.sha384(form.password.data.encode()).hexdigest()
        data = {
            "email": email,
            "password":password
        }
        # params = [{username: user, password: password}]
        # r = request.post("URL", params="")
        # data = r.json()
        return ("LOGGED IN")
    return render_template("login.html", form=form)

@app.route('/register.html', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)
    if form.validate_on_submit():
        first_name = form.name_first.data
        last_name = form.name_last.data
        email = form.email.data
        password = hashlib.sha384(form.password.data.encode()).hexdigest()
        today = datetime.datetime.now().isoformat()
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password":password,
            "time": today
        }
        print (data)
        
        return ('REGISTERED')
    return render_template("register.html", form=form)



if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=port)