from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean, LargeBinary
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

    def __init__(self, project_name, project_desc):
        self.project_name = project_name
        self.project_desc = project_desc
        db.session.add(Folder(foldername=project_name, project=self))

    @property
    def created(self):
        return local_time(self.created_at).strftime("%b %d %Y, %H:%M:%S")

    @property
    def updated(self):
        return local_time(self.updated_at).strftime("%b %d %Y, %H:%M:%S")

    @property
    def project_owner(self):
        return self.owner[0].full_name

    def collaborator_token(self, user, expires=7):
        return jwt.encode(
            {
                'project_id': self.id.hex,
                'user_id': user.id.hex,
                'exp': datetime.now(tz=timezone.utc) + timedelta(days=expires)
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

    @property
    def root_folder(self):
        for folder in self.folders:
            if folder.foldername == self.project_name:
                return folder
        return None

    def has_access(self, user, folder):
        return self in user.projects and folder.project == self

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


class Folder(db.Model):
    __tablename__ = 'folder'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index=True,
                default=uuid.uuid4)

    foldername = Column(String(50),
                  index=True,
                  nullable=False)

    parent_id = Column(UUIDType(binary=False),
                     ForeignKey('folder.id'))

    project_id = Column(UUIDType(binary=False),
                     ForeignKey('project.id'))

    children = relationship('Folder',
                backref=backref('parent', remote_side=[id]))

    project = relationship('Project',
                backref=backref('folders', cascade='all, delete-orphan'))

    files = relationship('File',
                        secondary='folder_content',
                        viewonly=True)

    @property
    def children_to_dict(self):
        return  [{'id': child.id.hex, 'name':child.foldername} for child in self.children]

    @property
    def files_to_dict(self):
        return [{'id': file.id.hex, 'name':file.filename} for file in self.files]

    @property
    def to_dict(self):
        children = self.children_to_dict
        files = self.files_to_dict
        return {
            'id': self.id.hex,
            'name': self.foldername,
            'parent_id': self.parent_id.hex if self.parent_id else None,
            'children': children,
            'files': files
        }

    def is_valid_folder(self, foldername):
        if not foldername:
            return False
        return not any(filter(lambda folder: folder.foldername == foldername, self.children))

    def is_valid_file(self, filename):
        if not filename:
            return False
        return not any(filter(lambda file: file.filename == filename, self.files))

    def __repr__(self):
        return f'<Folder: {self.foldername}>'


class File(db.Model):
    __tablename__ = 'file'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index=True,
                default=uuid.uuid4)

    filename = Column(String(50),
                  index=True)

    data = Column(LargeBinary)

    folders = relationship('Folder',
                           secondary='folder_content',
                           viewonly=True)

    def __repr__(self):
        return f'<File: {self.filename}>'


class FolderContent(db.Model):
    __tablename__ = 'folder_content'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index=True,
                default=uuid.uuid4)

    folder_id = Column(UUIDType(binary=False),
                     ForeignKey('folder.id'))

    file_id = Column(UUIDType(binary=False),
                     ForeignKey('file.id'))

    folder = relationship(Folder, backref='folder_content')
    file = relationship(File, backref='folder_content')
