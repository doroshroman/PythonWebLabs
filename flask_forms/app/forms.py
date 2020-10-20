from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, AnyOf

class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired('A username is required'),
        Length(min=4, max=20, message='Must be between 4 and 20')
        ])
    password = PasswordField('password', validators=[
        InputRequired('A password is required'),
        AnyOf(['admin', 'password', 'secret'])
        ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')