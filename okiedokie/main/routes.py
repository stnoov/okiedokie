from flask import Blueprint
import datetime, sys
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required
from okiedokie import db
from okiedokie.models import Events, Reviews, News, User
from flask_login import current_user
from okiedokie.meetings.forms import CreateEventForm
from okiedokie.main.forms import YandexPaymentForm, AddReviewForm, CreateNewsForm


main = Blueprint('main', __name__)


@main.route('/home', methods=['GET', 'POST'])
@main.route('/meetings', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def home():
    events = Events.query.order_by(Events.date.desc())
    news = News.query.order_by(News.date.desc())
    current_date = datetime.datetime.now()
    form = CreateEventForm()
    news_form = CreateNewsForm()
    form_action = request.args.get('form_action', 1)
    if news_form.validate_on_submit() and form_action == 'news':
        news_entry = News(title=news_form.title.data, date=current_date, text=news_form.text.data)
        db.session.add(news_entry)
        db.session.commit()
        flash('News has been added!', 'success')
        return redirect(url_for('main.home'))
    elif current_user.is_authenticated:
        if current_user.is_admin and form.validate_on_submit() and form_action == 'event':
            event_date = datetime.datetime(
                *[int(v) for v in form.date.data.replace('T', '-').replace(':', '-').split('-')])
            new_event = Events(title=form.title.data, date=event_date, duration=form.duration.data,
                               places=form.places.data,
                               text=form.text.data, zoom_link=form.zoom_link.data)
            db.session.add(new_event)
            db.session.commit()
            flash('Event has been created', 'success')
            return redirect(url_for('main.home'))

    return render_template('home.html', events=events, current_date=current_date, form=form, news_form=news_form, news=news)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')


@main.route('/payment', methods=['GET', 'POST'])
def payment():
    form = YandexPaymentForm()
    return render_template('payment.html', form=form)


@main.route('/okiepoints')
def okiepoints():
    top_users = User.query.order_by(User.points.desc()).limit(5).all()
    return render_template('okiepoints.html', top_users=top_users)


@main.route('/reviews', methods=['GET', 'POST'])
def reviews():
    page = request.args.get('page',1, type=int)
    reviews = Reviews.query.order_by(Reviews.date.desc()).paginate(page=page, per_page=5)
    current_date = datetime.datetime.now()
    form = AddReviewForm()
    if form.validate_on_submit():
        new_review = Reviews(title=form.title.data, text=form.text.data, date=current_date,
                             author=current_user)
        db.session.add(new_review)
        db.session.commit()
        flash('Review has been submitted!', 'success')
        return redirect(url_for('main.reviews'))
    return render_template('reviews.html', reviews=reviews, form=form, current_date=current_date)


@main.route("/home/<int:news_id>/delete_news/", methods=['GET', 'POST'])
@login_required
def delete_news(news_id):
    if current_user.is_admin:
        news = News.query.get_or_404(news_id)
        db.session.delete(news)
        db.session.commit()
        flash('News has been deleted!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('You do not have permissions to do that', 'danger')
        return redirect(url_for('main.home'))


@main.route("/home/<int:review_id>/delete_review/", methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    if current_user.is_admin:
        review = Reviews.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        flash('Review has been deleted!', 'success')
        return redirect(url_for('main.reviews'))
    else:
        flash('You do not have permissions to do that', 'danger')
        return redirect(url_for('main.home'))

