from flask import Blueprint, render_template, request, current_app, session
from flask_login import current_user
from okiedokie import db
from okiedokie.models import Payments, User
from flask_login import login_required
import hashlib
import sys


ya_payments = Blueprint('ya_payments', __name__)


@ya_payments.route('/products')
def payment():
    return render_template('products.html')


@ya_payments.route('/payment/success')
def success():
    return render_template('success.html')


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
        payment = Payments(date=request.form['datetime'], amount=request.form['amount'], user_id=request.form['label'], confirmed=False)
        db.session.add(payment)
        db.session.commit()
        exit()
    else:
        rounded = round(float(request.form['amount']))
        payment = Payments(date=request.form['datetime'], amount=request.form['amount'], user_id=request.form['label'], confirmed=True)
        user = User.query.filter_by(id=int(request.form['label'])).first()
        db.session.add(payment)
        db.session.commit()
        print(payment.product)
        print(request.form['label'])
        if int(rounded) == int(157):
            print(rounded)
            user.paid_classes = user.paid_classes + 1
            payment.product = '1 class'
            db.session.commit()
        elif int(rounded) == int(735):
            print(rounded)
            user.paid_classes = user.paid_classes + 5
            payment.product = '5 classes'
            db.session.commit()
        elif int(rounded) == int(1372):
            user.paid_classes = user.paid_classes + 10
            payment.product = '10 classes'
            db.session.commit()
        print('after')
        return request.form['amount']
