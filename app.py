from datetime import time
import os

from flask import Flask, request, render_template
from models import RegForm, LoginForm
from flask_bootstrap import Bootstrap
import hashlib
import datetime
import requests, json

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
        
        params = {"data": {"email": "aaa@gmial.com",    
                       "password": "*71237**123712383"
                       },
              "request": "login"}
        res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access', json=params)
        # data = res.json()
        print(res.text)
        return ("LOGGED IN")
    return render_template("login.html", form=form)

@app.route('/register.html', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)
    if form.validate_on_submit():
        first_name = form.name_first.data
        last_name = form.name_last.data
        email = form.email.data
        username = form.user_name.data
        password = hashlib.sha384(form.password.data.encode()).hexdigest()
        params = {"data": {"email": email,
                       "password": password,
                       "username": username,
                       "firstname": first_name,
                       "lastname": last_name},
              "request": "login"}
        # print(params)
        res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access', json=params)
        # data = json.load(res)
        print(res.text)        
        return ('REGISTERED')
    return render_template("register.html", form=form)



if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=port)