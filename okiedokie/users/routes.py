from flask import Blueprint, current_app, session
import datetime
from flask import render_template, url_for, flash, redirect, request
from okiedokie import db, bcrypt
from okiedokie.models import User
from flask_login import login_user, current_user, logout_user, login_required
from okiedokie.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from okiedokie.users.utils import send_reset_email, send_confirmation_email, save_picture


users = Blueprint('users', __name__)


@users.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    age=form.age.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash('Письмо с подтверждением было отправлено на вашу почту!', 'success')
        return redirect(url_for('users.sign_in'))
    return render_template('sign_up.html', form=form)


@users.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                if not user.confirmed:
                    flash('Please, confirm your email first.', 'danger')
                    return redirect(url_for('users.sign_in'))
                login_user(user, remember=form.remember.data)
                return redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('sign_in.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    current_date = datetime.datetime.now()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    return render_template('profile.html', form=form, current_date=current_date, image_file=image_file)


@users.route('/confirm/<token>')
def confirm_token(token):
    user = User.verify_confirmation_token(token)
    if not user:
        flash('The token is invalid or expired', 'danger')
        return redirect(url_for('main.home'))
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))


@users.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Message with instruction was sent to your email', 'info')
        return redirect(url_for('users.sign_in'))
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('The token is invalid or expired', 'danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.sign_in'))
    return render_template('reset_token.html', form=form)



