from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = StringField('Date and Time', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    places = IntegerField('Places', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    zoom_link = StringField('Zoom', validators=[DataRequired()])
    submit = SubmitField('Create Event')


class EventSignUp(FlaskForm):
    submit = SubmitField('Sign Up')