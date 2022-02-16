from flask import Flask


def create_app(environment='development'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config.get(environment))

    @app.route('/welcome')
    def welcome():
        return 'Welcome to Flask!'

    return app