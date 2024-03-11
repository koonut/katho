import os



class Config:
    SECRET_KEY = 'password'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://avnadmin:AVNS_oemweulDq4kiR6uMeHD@mysql-2f1d03e1-mca-c271.a.aivencloud.com:21594/katho'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
