from flask import Blueprint, current_app, request, session
import datetime
from flask import render_template, url_for, flash, redirect
from okiedokie import db
from okiedokie.models import User, Events
from flask_login import current_user, login_required
from okiedokie.meetings.forms import EventSignUp
from okiedokie.meetings.utils import send_notification_email

meetings = Blueprint('meetings', __name__)


@meetings.route("/meetings/<int:event_id>", methods=['GET', 'POST'])
@login_required
def event(event_id):
    event = Events.query.get_or_404(event_id)
    form = EventSignUp()
    event1 = Events.query.filter_by(id=event_id).first()
    current_date = datetime.datetime.now()
    timedelta = event1.date - current_date
    total_seconds = timedelta.total_seconds()
    minutes = total_seconds / 60
    registered = False
    for user in event1.signed_users:
        if current_user.id == user.id:
            registered = True
    if form.validate_on_submit():
        if registered and not current_user.is_admin:
            flash('You are already signed  for this meeting', 'warning')
            return redirect(url_for('main.home'))
        if current_user.paid_classes < 1:
            flash('You eventsnot have enough classes to register', 'warning')
            return redirect(url_for('main.home'))
        event.signed_users.append(current_user)
        send_notification_email(current_user, event1)
        event.places = event.places - 1
        current_user.paid_classes = current_user.paid_classes - 1
        current_user.attended_classes = current_user.attended_classes + 1
        db.session.commit()
        flash('You have signed up for the meeting', 'success')
        return redirect(url_for('main.home'))
    return render_template('event.html', event=event, form=form, current_date=current_date,
                           registered=registered, minutes=minutes)



@meetings.route("/meetings/<int:event_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(event_id):
    if current_user.is_admin:
        post = Events.query.get_or_404(event_id)
        post.deleted = True
        db.session.commit()
        flash('Event has been deleted!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('You do not have permissions to do that', 'danger')
        return redirect(url_for('main.home'))