from flask_wtf import FlaskForm, RecaptchaField
from wtforms import validators
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from okiedokie.models import User


class RegistrationForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20), validators.Regexp('^\w+$', message="Firstname must contain only letters")])
    last_name = StringField('Last name', [validators.DataRequired(), validators.Length(min=2, max=40), validators.Regexp('^\w+$', message="Lastname must contain only letters")])
    age = IntegerField('Age', [validators.DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered!')


class LoginForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    email = EmailField('Email address', [validators.Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'],
                                                                          message="Only jpg and png images are allowed")])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please, register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
