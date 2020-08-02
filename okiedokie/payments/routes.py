from flask import Blueprint, render_template, request
from flask_login import current_user
import hashlib
import sys


payments = Blueprint('payments', __name__)


@payments.route('/ya_payment')
def payment():
    return render_template('payment.html',user_email=current_user.email)


@payments.route('/ya_payment/success')
def success():
    return "Оплата прошла успешно"


@payments.route('/ya_payment/notifications', methods=['POST'])
def notification():
    hash2 = request.form['notification_type'] + '&' + request.form['operation_id'] \
            + '&' + request.form['amount'] + '&' + request.form['currency'] + '&' + \
            request.form['datetime'] + '&' + request.form['sender'] + '&' + \
            request.form['codepro'] + '&' + 'JNISfRip1K8HekP+U0uwyVR3' + '&' + request.form['label']

    hash = hashlib.sha1(str(hash2).encode('utf-8')).hexdigest()

    if hash == request.form['sha1_hash']:
        print(hash + " Сумма " + request.form['amount'] + " " + request.form['label'], file=sys.stderr)

    # if request.form['sha1_hash'] != hash or request.form['codepro'] or request.form['unaccepted']:
    #     print('Fail!', file=sys.stderr)
    #     return "Fail"