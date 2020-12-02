import hashlib
from hashlib import new
import json
import os
from datetime import time
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
            print ("File size more then 10Mb.")
            status="File size more then 10Mb."

        elif '.' in file.filename and file.filename.split('.', 1)[1] not in ALLOWED_EXTENSIONS:
            print("This file extesion not allowed.")
            status="This file extesion not allowed."

        else:
            try:
                thumbnail_bucket_name = "videos_thumbnail"
                bucket_name = "videos_360"
                # source_file_name = "local/path/to/file"
                print(file.filename)

                destination_blob_name = file.filename

                # Creating thumbnail file:

                print(file.stream)


                # vs = file.stream
                # image_name = destination_blob_name.split('.')[0] + '.jpeg'
                # frame = vs.get_frame_at_sec(10)
                # img = frame.image()
                # img = img.resize((300, 300))
                # img.save('{0}.jpeg'.format(image_name))

                # linking storage
                storage_client = storage.Client.from_service_account_json(
                    'C:/Users/nisch/Downloads/cloudcomputinglab-291822-bf0774247e88.json')
                # storage_client = storage.Client.from_service_account_json(
                #     'C:/Users/Naveen S N/Downloads/CloudComputingLab-745a59e0bb6e.json')

                # Uploading thumbnail
                # Setting destination name
                thumbnail_bucket = storage_client.bucket(thumbnail_bucket_name)
                # thumbnail_blob = thumbnail_bucket.blob(image_name)

                # thumbnail_blob.upload_from_file(img)

                # uploading video file
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)

                blob.upload_from_file(file)

                print(
                    "File {} uploaded to {}.".format(
                        file.filename, destination_blob_name
                    )
                )

                filename = file.filename,
                status = "Uploaded"

            except Exception as e:
                print(e)
                status="Failed to upload. Some error occured."

        return render_template('upload.html', message=status)
    return render_template('upload.html')

@app.route('/view/', methods=['GET', 'POST'])
def view():
    return render_template('view.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=port)
