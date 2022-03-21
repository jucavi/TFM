from app import db
from sqlalchemy import Column, LargeBinary, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType
import uuid


class Folder(db.Model):
    __tablename__ = 'folder'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index = True,
                default=uuid.uuid4)

    foldername = Column(String(50),
                  index=True)

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


class File(db.Model):
    __tablename__ = 'file'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index = True,
                default=uuid.uuid4)

    filename = Column(String(50),
                  index=True)

    data = Column(LargeBinary)

    folders = relationship('Folder',
                           secondary='folder_content',
                           viewonly=True)


class FolderContent(db.Model):
    __tablename__ = 'folder_content'

    id = Column(UUIDType(binary=False),
                primary_key=True,
                index = True,
                default=uuid.uuid4)

    folder_id = Column(UUIDType(binary=False),
                     ForeignKey('folder.id'))

    file_id = Column(UUIDType(binary=False),
                     ForeignKey('file.id'))

    folder = relationship(Folder, backref='folder_content')
    file = relationship(File, backref='folder_content')