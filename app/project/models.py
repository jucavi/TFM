from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
import uuid
from datetime import datetime


class Project(db.Model):

    __tablename__ = 'project'
    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    project_name = Column(
        String(40),
        index = True,
        unique=True,
        nullable = True
    )
    project_desc = Column(
        Text(),
        nullable = True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship(
        'User', secondary='team',
        primaryjoin=('and_(Project.id==Team.project_id, Team.is_owner==True)'),
        viewonly=True)

    collaborators = relationship(
        'User', secondary='team',
        primaryjoin=('and_(Project.id==Team.project_id, Team.is_owner==False)'),
        viewonly=True)

    def __repr__(self):
        return f'<Project: {self.project_name!r}>'


class Team(db.Model):
    __tablename__ = 'team'

    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    user_id = Column(UUIDType(binary=False), ForeignKey('user.id'))
    project_id = Column(UUIDType(binary=False), ForeignKey('project.id'))
    is_owner = Column(Boolean, default=False)

    user = relationship('User', backref=backref('teams'), lazy=True)
    project = relationship('Project', backref=backref('team', cascade='all, delete-orphan'))
