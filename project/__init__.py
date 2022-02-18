from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
crsf = CSRFProtect()


def create_app(environment='develop'):
    from config import config


    app = Flask(__name__)
    app.config.from_object(config.get(environment))

    db.init_app(app)
    migrate.init_app(app, db)
    crsf.init_app(app)

    with app.app_context():
        from .home import home
        from .auth import auth

        app.register_blueprint(home.home_bp)
        app.register_blueprint(auth.auth_bp)

    return app