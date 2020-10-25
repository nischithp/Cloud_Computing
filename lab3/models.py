
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators
from flask_wtf import Form

class RegForm(Form):
  name_first = StringField('First Name', 
                 [validators.DataRequired()])
  name_last = StringField('Last Name', 
                 [validators.DataRequired()])
  email = StringField('Email Address', [validators.DataRequired(), 
             validators.Email(), validators.Length(min=6, max=35)])
  password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', 
                           message='Passwords must match')
        ])
  confirm = PasswordField('Repeat Password')
  submit = SubmitField('Submit')

class LoginForm(Form):
    first_name = StringField(u'First Name', validators=[validators.input_required()])
    last_name  = StringField(u'Last Name', validators=[validators.optional()])

