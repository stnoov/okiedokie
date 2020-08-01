from datetime import datetime
from flask import abort, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from okiedokie import db, login_manager, admin
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


signed_users = db.Table('signed_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    points = db.Column(db.Integer, default=0)
    paid_classes = db.Column(db.Integer, default=1)
    attended_classes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Reviews', backref='author', lazy=True)
    signed_users = db.relationship('Events', secondary=signed_users, lazy='subquery',
        backref=db.backref('signed_users', lazy=True))

    #### CONFIRM EMAIL ####
    def get_confirmation_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    #### RESET PASSWORD ####
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=False)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    places = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    zoom_link = db.Column(db.String(255), nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return current_user.is_authenticated
        else:
            return abort(404)


admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Events, db.session))
admin.add_view(Controller(Reviews, db.session))
admin.add_view(Controller(News, db.session))



