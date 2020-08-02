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
    return render_template('payment.html',user_id=current_user.id)


@ya_payments.route('/payment/success')
def success():
    return "Оплата прошла успешно"


@ya_payments.route('/ya_payment/notifications', methods=['POST'])
def notification():
    hash2 = request.form['notification_type'] + '&' + request.form['operation_id'] \
            + '&' + request.form['amount'] + '&' + request.form['currency'] + '&' + \
            request.form['datetime'] + '&' + request.form['sender'] + '&' + \
            request.form['codepro'] + '&' + 'f9R1OVrbXU1QRv9STHXPNq81' + '&' + request.form['label']

    hash = hashlib.sha1(str(hash2).encode('utf-8')).hexdigest()

    if ( str(request.form['sha1_hash']) != str(hash) ) or ( request.form['codepro'] == True):
        print( request.form['sha1_hash'], hash, 'FAIL', file=sys.stderr)
        exit()
    else:
        payment = Payments(date=request.form['datetime'], amount=request.form['amount'], product=request.form['formcomment'], user_id=request.form['label'])
        db.session.add(payment)
        db.session.commit()
        user = User.query.filter_by(id=payment.user_id).first()
        if payment.user_id:
            if payment.product == '1 class':
                user.paid_classes = user.paid_classes + 1
            elif payment.product == '5 classes':
                user.paid_classes = user.paid_classes + 5
            elif payment.product == '10 classes':
                user.paid_classes = user.paid_classes + 10
            db.session.commit()

    return 'Payment in process'
