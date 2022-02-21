from project import db
from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid

class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(
        UUIDType(binary=False),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    firstname = db.Column(
        db.String(40),
        index = True,
        nullable = False
    )
    lastname = db.Column(
        db.String(40),
        index = True,
        nullable = False
    )
    username = db.Column(
        db.String(40),
        index = True,
        unique = True,
        nullable = False
    )
    email = db.Column(
        db.String(40),
        index = True,
        unique = True,
        nullable = False
    )
    password = db.Column(
        db.String(250),
        index = True,
        unique=False,
        nullable=False
	)


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'User {self.username}'
