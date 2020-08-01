import os

class Config:
    SECRET_KEY= '5791628bb0b13ce0c676dfde280ba245'
    BABEL_DEFAULT_LOCALE = 'en'
    LANGUAGES = ['en', 'ru']
    SQLALCHEMY_DATABASE_URI= 'sqlite:///site.db'
    MAIL_SERVER= 'smtp.googlemail.com'
    MAIL_PORT= '587'
    MAIL_USE_TLS= True
    MAIL_USERNAME= os.environ.get('GMAIL_LOGIN')
    MAIL_PASSWORD= os.environ.get('GMAIL_PASS')