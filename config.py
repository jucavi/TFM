from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY', 'Remember set your secret key!')
    FLASK_APP = environ.get('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'production.db')



class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'development.db')


config = dict(
    develop=DevConfig,
    production=ProdConfig
)
