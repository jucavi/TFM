from project import db
from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
from datetime import datetime, timezone, timedelta
from flask import current_app
import jwt

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


    def set_reset_password_token(self, expires=600):
        return jwt.encode(
            {
                'reset_password': self.id.hex,
                'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expires)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )


    @staticmethod
    def check_resert_password_token(token):
        try:
            _id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])['reset_password']
            user_id = uuid.UUID(_id)
        except Exception:
            return None

        return User.query.get(user_id)


    def __repr__(self):
        return f'User {self.username}'
