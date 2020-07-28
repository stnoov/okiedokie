from okiedokie import  mail
from flask_mail import Message


def send_notification_email(user, event):
    msg = Message('Запись на занятие', sender='noreply@okiedokie.com',
                  recipients=[user.email])
    msg.body = \
        f'''
Вы успешно записали на занятие #{event.id}:

Занятие состоится: {event.date}
Ссылку на конференцию в Zoom вы сможете найти на странице занятия за 15 минут до его начала.

С уважением,
Админинистрация OkieDokie!
            '''

    mail.send(msg)