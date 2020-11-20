from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

url = 'http://127.0.0.1:8080/'
dictToSend = {"data": {"email": "aaa@gmial.com",
                       "password": "71237**123712383",
                       "username": "123",
                       "firstname": "123",
                       "lastname": "123"},
              "request": "login"}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            url = 'http://127.0.0.1:8080/'
            files = {'file': open(uploaded_file.filename, 'rb')}

            r = requests.post(url, files=files, json=dictToSend)
            r.text
            print(request.files['file'])
            uploaded_file.save(uploaded_file.filename)
            return render_template('index.html', message=r.text)
        return redirect(url_for('index'))
    return render_template('index.html')
