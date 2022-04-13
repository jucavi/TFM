from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY', 'Remember set your secret key!')
    FLASK_APP = environ.get('FLASK_APP')

    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = True

    # Mailtrap conf
    # MAIL_SERVER = 'smtp.mailtrap.io'
    # MAIL_PORT = 2525
    # MAIL_USERNAME = '8d723d7c957936'
    # MAIL_PASSWORD = '83ebc0b9992ffd'
    # MAIL_DEFAULT_SENDER = 'tft@mailtrap.io'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False



class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', '').replace("postgres://", "postgresql://", 1)



class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

    # Mailtrap conf
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '8d723d7c957936'
    MAIL_PASSWORD = '83ebc0b9992ffd'
    MAIL_DEFAULT_SENDER = 'tft@mailtrap.io'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


config = dict(
    develop=DevConfig,
    production=ProdConfig
)
