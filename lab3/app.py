import os
from flask import Flask, render_template
from forms import (
    LoginForm, RegistrationForm
)
from flask import Flask, request, render_template
from models import RegForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('pong.html')
    return render_template("login.html", form=form)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.email
        return ("LOGGED IN")
    return render_template("login.html", form=form)

@app.route('/register.html', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('REGISTERED')
    return render_template("register.html", form=form)



if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=port)