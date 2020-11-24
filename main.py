import hashlib
from hashlib import new
import json
import os
from datetime import time
from flask.helpers import flash

import requests
from flask import Flask, render_template, request, session
from requests.api import post
# from requests.sessions import session
from flask_bootstrap import Bootstrap


from models import EditProfileForm, LoginForm, RegForm

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)

# Constants
indexURL = "index.html"
registerURL = "register.html"
loginURL = "login.html"
editprofileURL = "editprofile.html"
userDataCloudURL = 'https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template(indexURL)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = hashlib.sha384(form.password.data.encode()).hexdigest()
        
        params = {"data": {"email": email,    
                       "password":password
                       },
              "request": "login"}
        res = requests.post(userDataCloudURL, json=params)
        data = {}
        print(res.text)
        # data = json.loads(res.text)
        status = res.status_code
        if(status==200):
            data = json.loads(res.text)
            putDataIntoSession(data)
            session["loggedin"] = True
            return render_template(indexURL)
        elif(status==401 or status==404):
            flash("Invalid credentials","error")
            form = LoginForm(request.form)
            return render_template(loginURL, form=form)
        elif status==500:
            return ("500 error. Please contact your server administrator.")
        return(data)
    return render_template(loginURL, form=form)

def putDataIntoSession(data):
    if "username" in data["data"]:
        print (data)
        session['id'] = data["data"]["id"]
        session['username'] = data["data"]['username']
        session['firstname'] = data["data"]['firstname']
        session['lastname'] = data["data"]['lastname']
        session['date_time'] = data["data"]['date_time']
        session['email'] = data["data"]['email']



@app.route('/register', methods=['GET', 'POST'])
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
              "request": "register"}
        res = requests.post(userDataCloudURL, json=params)
        data = {}
        data = json.loads(res.text)
        status = res.status_code
        if( status == 200):
            return render_template(loginURL)
        elif status == 403:
            flash("Email already in use. Please use another email")
        elif(status==500):
            return ("500 error. Please contact your server administrator.")
    return render_template(registerURL, form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template(indexURL)

@app.route('/editProfile', methods=['GET', 'POST'])
def editprofile():
    form = EditProfileForm(request.form)
    if form.validate_on_submit():
        oldPassword = hashlib.sha384(form.oldPassword.data.encode()).hexdigest()
        newPassword = hashlib.sha384(form.newPassword.data.encode()).hexdigest()
        confirmPassword = hashlib.sha384(form.confirm.data.encode()).hexdigest()
        if confirmPassword == newPassword:
            params = {
                "request": "update",
                "data": {
                    "id" : session['id'],
                    "oldPassword": oldPassword,
                    "newPassword": newPassword 
                }
            }
            res = requests.post(userDataCloudURL, json=params)
            data = {}
            if res.status_code == 200:
                # Success
                print(data)
                data = json.loads(res.text)
            elif res.status_code == 500:
                # INternl Server Error
                data = json.loads(res.text)
            elif res.status_code == 422:
                # Missing or Invalid Data
                data = json.loads(res.text)
            elif res.status_code == 401:
                # old and new passwords do not match
                data = json.loads(res.text)
            elif res.status_code == 404:
                # You can only login, register or editProfile
                data = json.loads(res.text)
            print("Response:"+res.text)
            # data = json.loads(res.text)
            status = res.status_code
            return data
    return render_template(editprofileURL, form=form)


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=port)
