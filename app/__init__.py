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
crsf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()

@click.command()
@with_appcontext
def populate():
    from app import seed

    print('Populating users:')
    print(f'Password for all users: {seed.PASSWORD!r}')
    seed.users()


def create_app(environment='develop'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config.get(environment))
    app.cli.add_command(populate)

    db.init_app(app)
    migrate.init_app(app, db)
    crsf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app.home import home
        from app.auth import auth
        from app.project import project

        from app.auth.user_model import User
        from app.project.project_model import Project, Team

        app.register_blueprint(home.home_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(project.project_bp, url_prefix='/projects')

    @app.shell_context_processor
    def make_shell_context():
       return {'db': db, 'mail': mail, 'app': app}


    return app


