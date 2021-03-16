import os


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    file = __file__
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'aed67f6a830450c078d051a123d980cf'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "riccardoaonline@gmail.com"
    MAIL_PASSWORD = "qwerty78987"
    FLASKY_ADMIN = 'ric@admin.com'

def conf(SQLALCHEMY_DATABASE_URI):
    percorso = SQLALCHEMY_DATABASE_URI
    return  percorso