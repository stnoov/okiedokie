from flask import url_for
from okiedokie import  mail
from flask_mail import Message


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@okiedokie.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not make your request, please ignore this email and no changes will be made.
    '''
    mail.send(msg)


def send_confirmation_email(user):
    token = user.get_confirmation_token()
    msg = Message('Please confirm your email.', sender='noreply@okiedokie.com',
                  recipients=[user.email])
    msg.body =\
    f'''Thank you for registration. Use the following link to activate your account:

    {url_for('users.confirm_token', token=token, _external=True)}

    If you did not make your request, please ignore this email and no changes will be made.
        '''

    mail.send(msg)