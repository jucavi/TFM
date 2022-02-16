from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(environment='develop'):
    from config import config


    app = Flask(__name__)
    app.config.from_object(config.get(environment))

    db.init_app(app)

    @app.route('/welcome')
    def welcome():
        return 'Welcome to Flask!'

    return app