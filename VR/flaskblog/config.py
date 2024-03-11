import os


class Config:
    SECRET_KEY = 'password'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/katho'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
