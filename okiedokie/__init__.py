from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
admin = Admin(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'englishclub.okiedokie'
app.config['MAIL_PASSWORD'] = 'Veron05Artem25'
mail = Mail(app)


from okiedokie.users.routes import users
from okiedokie.meetings.routes import meetings
from okiedokie.main.routes import main

app.register_blueprint(users)
app.register_blueprint(meetings)
app.register_blueprint(main)



