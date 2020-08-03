from okiedokie import mail
from flask_mail import Message


def send_contact_message(email, name, message):
    msg = Message('ВАЖНО! Новое сообщение.', sender='englishclub.okiedokie@okiedokie.com',
                  recipients=['englishclub.okiedokie@gmail.com'])
    msg.body =\
    f''' Пользователь {name}, отправил сообщение

    {message}

    Овет перенаправить на {email}
        '''

    mail.send(msg)