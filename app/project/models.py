from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
import uuid
from datetime import datetime, timedelta, timezone
from flask import current_app
import jwt
from app.helpers.date import local_time


class Project(db.Model):
    __tablename__ = 'project'
    id = Column(UUIDType(binary=False),
                primary_key=True,
                index = True,
                default=uuid.uuid4)

    project_name = Column(String(40),
                          index = True,
                          unique=True,
                          nullable = True)

    project_desc = Column(Text(),
                          nullable = True)

    created_at = Column(DateTime,
                        default=datetime.utcnow)

    updated_at = Column(DateTime,
                        default=datetime.utcnow)

    owner = relationship('User',
                         secondary='team',
                         primaryjoin=('and_(Project.id==Team.project_id, Team.is_owner==True)'),
                         viewonly=True)

    collaborators = relationship('User',
                                 secondary='team',
                                 primaryjoin=('and_(Project.id==Team.project_id, Team.is_owner==False)'),
                                 viewonly=True)

    @property
    def created(self):
        return local_time(self.created_at)

    @property
    def updated(self):
        return local_time(self.updated_at)

    def collaborator_token(self, user, expires=604800):
        return jwt.encode(
            {
                'project_id': self.id.hex,
                'user_id': user.id.hex,
                'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expires)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def project_collaborator_token(token):
        try:
            p_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['project_id']
            u_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
            project_id = uuid.UUID(p_id)
            user_id = uuid.UUID(u_id)
        except Exception:
            return None

        return project_id, user_id

    def __repr__(self):
        return f'<Project: {self.project_name!r}>'


class Team(db.Model):
    __tablename__ = 'team'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index = True,
                default=uuid.uuid4)

    user_id = Column(UUIDType(binary=False),
                     ForeignKey('user.id'))

    project_id = Column(UUIDType(binary=False),
                        ForeignKey('project.id'))

    is_owner = Column(Boolean,
                      default=False)

    user = relationship('User',
                        backref=backref('teams'),
                        lazy=True)
    project = relationship('Project',
                           backref=backref('team', cascade='all, delete-orphan'))
