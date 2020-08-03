import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from flask_babelex import Babel, gettext
from okiedokie.config import Config
from flask_admin.base import MenuLink



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin()
mail = Mail()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    from okiedokie.users.routes import users
    from okiedokie.meetings.routes import meetings
    from okiedokie.main.routes import main
    from okiedokie.ya_payments.routes import ya_payments

    app.register_blueprint(users)
    app.register_blueprint(meetings)
    app.register_blueprint(main)
    app.register_blueprint(ya_payments)
    admin.add_link(MenuLink(name='Back Home', url='/', category='Links'))
    return app


from okiedokie.models import User
def init_db():
    with create_app().app_context():
        db.drop_all()
        db.create_all()
        admin_pass = os.environ.get('ADMIN_PASS')
        hashed_password = bcrypt.generate_password_hash(admin_pass).decode('utf-8')
        user = User(email='stnoov@gmail.com', first_name="Artem", last_name="Sitnov", is_admin=True,
                    age=0, confirmed=True, password=hashed_password)
        db.session.add(user)
        db.session.commit()


