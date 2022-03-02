from app import db
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
from flask import current_app
import jwt

class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    firstname = Column(
        String(40),
        index = True,
        nullable = False
    )
    lastname = Column(
        String(40),
        index = True,
        nullable = False
    )
    username = Column(
        String(40),
        index = True,
        unique = True,
        nullable = False
    )
    email = Column(
        String(40),
        index = True,
        unique = True,
        nullable = False
    )
    password = Column(
        String(250),
        index = True,
        unique=False,
        nullable=False
	)

    projects = relationship(
        'Project',
        secondary='team',
        viewonly=True
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


    # @property
    # def projects_owner(self):
    #     projects = self.projects
    #     owner = [project for project in projects if project.owner and self == project.owner[0]]
    #     return owner

    # @property
    # def projects_owner(self):
    #     projects = self.projects
    #     owner = [project for project in projects if project.owner and self == project.owner[0]]
    #     return owner



    @staticmethod
    def check_resert_password_token(token):
        try:
            _id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
            user_id = uuid.UUID(_id)
        except Exception:
            return None

        return User.query.get(user_id)



    projects_owner = relationship(
        'Project',
         secondary='team', primaryjoin=('and_(User.id==Team.user_id, Team.is_owner==True)'),
          viewonly=True
        )
    projects_guest = relationship(
        'Project',
         secondary='team', primaryjoin=('and_(User.id==Team.user_id, Team.is_owner==False)'),
          viewonly=True
        )



    def __repr__(self):
        return f'<User: {self.username!r}>'
