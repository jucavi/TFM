from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
import click
from flask.cli import with_appcontext


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()

@click.command()
@with_appcontext
def populate():
    from app import seed
    seed.seed()


def create_app(environment='develop'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config.get(environment))
    app.cli.add_command(populate)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # routes
        from app.home import home
        from app.auth import auth
        from app.project import project
        from app.message import message
        from app.errors import handler


        # models
        from app.auth.models import User
        from app.project.models import Project, Team
        from app.message.models import Message

        #blueprints
        app.register_blueprint(home.home)
        app.register_blueprint(auth.auth)
        app.register_blueprint(project.projects, url_prefix='/projects')
        app.register_blueprint(message.messages)
        app.register_blueprint(handler.errors)


    @app.shell_context_processor
    def make_shell_context():
       return {'db': db,
               'User': User,
               'Project': Project,
               'Team': Team,
               'Message': Message
               }

    return app


