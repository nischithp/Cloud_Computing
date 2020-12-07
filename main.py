import hashlib
from hashlib import new
import json
import os
from datetime import datetime, time
from flask.helpers import flash

import requests
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from requests.api import post
# from requests.sessions import session
from flask_bootstrap import Bootstrap
from PIL import Image
from google.cloud import storage
from moviepy.editor import VideoFileClip


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
    # linking storage
    storage_client = storage.Client.from_service_account_json(
                    'C:/Users/nisch/Downloads/cloudcomputinglab-291822-bf0774247e88.json')
    bucket_name = "videos_360"
    videoNames = storage_client.list_blobs(bucket_name)

    bucket_name="videos_thumbnail"
    thumbnails = storage_client.list_blobs(bucket_name)

    # for blob in blobs:
    #     print(blob.name)    
    return render_template(indexURL, videoNames=videoNames, thumbnails=thumbnails)


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
            return redirect("/")
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
        print(res)
        if status == 201:
            flash("Succesful registration. Please proceed to login")
            # form = LoginForm(request.form)
            return redirect("/login")
        elif status == 403:
            flash("Email already in use. Please use another email")
        elif status == 500:
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
                flash("Password updated")
                data = res.text
            elif res.status_code == 500:
                # INternl Server Error
                data = res.text
            elif res.status_code == 422:
                # Missing or Invalid Data
                data = res.text
            elif res.status_code == 401:
                # old and new passwords do not match
                data = res.text
            elif res.status_code == 404:
                # You can only login, register or editProfile
                data = res.text
            print("Response:"+res.text)
            # data = json.loads(res.text)
            status = res.status_code
            return data
    return render_template(editprofileURL, form=form)

url = 'http://127.0.0.1:8080/'
dictToSend = {"data": {"email": "aaa@gmial.com",
                       "password": "71237**123712383",
                       "username": "123",
                       "firstname": "123",
                       "lastname": "123"},
              "request": "login"}

ALLOWED_SIZE = 100*1024*1024*1024
ALLOWED_EXTENSIONS = set(['mpg', 'mpeg', 'mp4'])


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        size = request.content_length

        if not file:
            print("No File to Upload.")
            status="No File to Upload."

        elif size > ALLOWED_SIZE:
            print ("File size more then 10GB.")
            status="File size more then 10GB."

        elif '.' in file.filename and file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
            print("This file extesion not allowed.")
            status="This file extesion not allowed."

        else:
            try:
                bucket_name = "videos_360"
                timestr = time.strftime("%Y%m%d-%H%M%S")
                destination_blob_name = str(session['id'])+ '-' + datetime.now().strftime("%Y%m%d%H%M%S") + '.' + file.filename.split('.')[-1]
                print(destination_blob_name)

                # linking storage
                storage_client = storage.Client.from_service_account_json(
                    'C:/Users/nisch/Downloads/cloudcomputinglab-291822-bf0774247e88.json')
                # storage_client = storage.Client.from_service_account_json(
                #     'C:/Users/Naveen S N/Downloads/CloudComputingLab-745a59e0bb6e.json')

                # uploading video file
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)

                metadata = {'title': file.filename, 'name': destination_blob_name }
                blob.metadata = metadata
                blob.upload_from_file(file)

                print(
                    "File {} uploaded to {}.".format(
                        file.filename, destination_blob_name
                    )
                )
                params = {
                "userid": session['id'],
                "video": {
                    "title" : file.filename,
                    "url": destination_blob_name
                    # "tag": "abcd",
                    # "description": "asdasdas",
                    # "privacy": "00000000000012"
                        }
                }
                # res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access', json=dictToSend)
                res = requests.post('http://127.0.0.1:8080/', json=params)
                if res.status_code == 200:
                    status = "Uploaded"             
                    # flash(status)

            except Exception as e:
                print(e)
                status="Failed to upload. An error occured."
                # flash(status)
        return render_template('upload.html')
    return render_template('upload.html')

@app.route('/view/<videoName>', methods=['GET', 'POST'])
def view(videoName):
    if request.method == 'GET':
        videoData = {"videoQuality" : 360,
                 "videoName": videoName}
        return render_template('view.html', videoData=videoData)
    return ("this page can only be reached with a GET request. Please click on a thumbnail on the home page")

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=False, host='0.0.0.0', port=port)
