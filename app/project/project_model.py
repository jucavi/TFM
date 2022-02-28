from app import db
from sqlalchemy_utils import UUIDType
import uuid
from datetime import datetime


user_projects = db.Table('user_projects',
    db.Column('user_id', UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False),
    db.Column('project_id', UUIDType(binary=False), db.ForeignKey('project.id'), nullable=False),
    db.Column('is_owner', db.Boolean, default=False)
)

class Project(db.Model):

    __tablename__ = 'project'
    id = db.Column(
        UUIDType(binary=False),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    projectname = db.Column(
        db.String(40),
        index = True,
        unique=True,
        nullable = False
    )
    projectdesc = db.Column(
        db.Text()
    )
    created_at = db.Column(
        db.DateTime,
        nullable = False
    )
    updated_at = db.Column(
        db.DateTime,
        nullable = False
    )
    users = db.relationship('User', secondary=user_projects, lazy='subquery', backref=db.backref('projects', lazy=True))

    def __init__(self, projectname):
        self.projectname = projectname
        self.created_at = self.updated_at = datetime.now()


    def __repr__(self):
        return f'<Project: {self.projectname!r} created_at: {self.created_at}>'
