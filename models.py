from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from flask_wtf import Form

class RegForm(Form):
  name_first = StringField('First Name', 
                 [validators.DataRequired()])
  name_last = StringField('Last Name')
  user_name = StringField('User Name')
  email = StringField('Email Address', [validators.DataRequired(), 
             validators.Email(), validators.Length(min=6, max=35)])
  password = PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
  confirm = PasswordField('Repeat Password')
  submit = SubmitField('Submit')

class LoginForm(Form):
  email = StringField('Email', [validators.InputRequired(),validators.Length(1, 64),validators.Email()])
  password = PasswordField('Password', [validators.InputRequired()])
  remember_me = BooleanField('Keep me logged in')
  submit = SubmitField('Log in')

class EditProfileForm(Form):
  oldPassword = PasswordField('Old Password', [validators.InputRequired()])
  newPassword = PasswordField('New Password', [validators.InputRequired()])
  confirm = PasswordField('Repeat Password',  [validators.DataRequired(),validators.EqualTo('newPassword', message='Passwords must match')])
  submit = SubmitField('Change Password')
<<<<<<< HEAD
=======



>>>>>>> 397d3bcc6027ad33e1fd18b0a9d65c53ab881242
