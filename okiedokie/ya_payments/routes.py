from flask import Blueprint, render_template, request
from flask_login import current_user
from okiedokie import db
from okiedokie.models import Payments, User
from flask_login import login_required
import hashlib
import sys


ya_payments = Blueprint('ya_payments', __name__)


@ya_payments.route('/products')
@login_required
def payment():
    return render_template('products.html', user_id=current_user.id)


@ya_payments.route('/payment/success')
def success():
    return "Оплата прошла успешно"


@ya_payments.route('/payment/notifications', methods=['POST'])
def notification():
    hash2 = request.form['notification_type'] + '&' + request.form['operation_id'] \
            + '&' + request.form['amount'] + '&' + request.form['currency'] + '&' + \
            request.form['datetime'] + '&' + request.form['sender'] + '&' + \
            request.form['codepro'] + '&' + 'f9R1OVrbXU1QRv9STHXPNq81' + '&' + request.form['label']

    hash = hashlib.sha1(str(hash2).encode('utf-8')).hexdigest()
    if ( str(request.form['sha1_hash']) != str(hash) ) or ( request.form['codepro'] == True):
        rounded = round(float(request.form['amount']))
        print(int(rounded))
        print(float(request.form['amount']))
        print(str(request.form['amount']))
        return request.form['amount']

        # payment = Payments(date=request.form['datetime'], amount=request.form['amount'], product=str(request.form['amount']), user_id=request.form['label'], confirmed=False)
        # db.session.add(payment)
        # db.session.commit()
        # exit()
    else:
        rounded = round(float(request.form['amount']))
        if rounded < 1000:
            print(rounded)
        return request.form['amount']
        # payment = Payments(date=request.form['datetime'], amount=request.form['amount'], product=str(request.form['amount']), user_id=int(request.form['label']), confirmed=True)
        # user = User.query.filter_by(id=int(request.form['label'])).first()
        # db.session.add(payment)
        # db.session.commit()
        # print(payment.product)
        # user.paid_classes = user.paid_classes + 5

