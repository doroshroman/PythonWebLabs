from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, ValidationError, Regexp

from .models import *

class FilmForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired(), Length(min=0, max=64)])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    budget = StringField('Budget', validators=[DataRequired(), Regexp('[0-9]+\.?[0-9]+')])
    genres = SelectField('Genre', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired(), Length(min=0, max=64)])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    budget = StringField('Budget', validators=[DataRequired(), Regexp('[0-9]+\.?[0-9]+')])
    genres = SelectField('Genre', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update')




