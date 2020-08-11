import os
import secrets
from flask import current_app
from PIL import Image
from flask import url_for
from okiedokie import mail
from flask_mail import Message


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Запрос восстановления пароля.', sender='englishclub.okiedokie@okiedokie.com',
                  recipients=[user.email])
    msg.body = f'''Чтобы восстановить пароль, перейдите по следующему адресу:

{url_for('users.reset_token', token=token, _external=True)}

С уважением,
OkieDokie!
    '''
    mail.send(msg)


def send_confirmation_email(user):
    token = user.get_confirmation_token()
    msg = Message('Подтверждение аккаунта.', sender='englishclub.okiedokie@okiedokie.com',
                  recipients=[user.email])
    msg.body =\
    f'''Спасибо за регистрацию, чтобы подтвердить аккаунт пройдите по следующей ссылке:

    {url_for('users.confirm_token', token=token, _external=True)}

Если у вас возникли проблемы, пожалуйста, обратитесь в поддержку, используя контактную форму на сайте.

С уважением,
OkieDokie!
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