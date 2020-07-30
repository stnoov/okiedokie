from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from okiedokie.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin()
mail = Mail()





def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    mail.init_app(app)

    from okiedokie.users.routes import users
    from okiedokie.meetings.routes import meetings
    from okiedokie.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(meetings)
    app.register_blueprint(main)

    return app


