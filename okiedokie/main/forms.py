from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp
from wtforms.fields.html5 import EmailField

class AddReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Add Review')


class CreateNewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    add = SubmitField('Add news')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Regexp('\w+', message="Name must contain only letters")])
    email = EmailField('Email', validators=[DataRequired()])
    message = TextAreaField('Message',validators=[DataRequired()])
    send = SubmitField('Send')
class YandexPaymentForm(FlaskForm):
    submit = SubmitField('Pay')