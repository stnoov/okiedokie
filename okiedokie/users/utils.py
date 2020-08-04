import os
import secrets
from flask import current_app
from PIL import Image
from flask import url_for
from okiedokie import mail
from flask_mail import Message


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='englishclub.okiedokie@okiedokie.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not make your request, please ignore this email and no changes will be made.
    '''
    mail.send(msg)


def send_confirmation_email(user):
    token = user.get_confirmation_token()
    msg = Message('Please confirm your email.', sender='englishclub.okiedokie@okiedokie.com',
                  recipients=[user.email])
    msg.body =\
    f'''Thank you for registration. Use the following link to activate your account:

    {url_for('users.confirm_token', token=token, _external=True)}


    If you did not make your request, please ignore this email and no changes will be made.
        '''

    mail.send(msg)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn