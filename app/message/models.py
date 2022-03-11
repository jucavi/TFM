from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column,DateTime, ForeignKey, Boolean
import uuid
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'message'

    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    sender_id = Column(UUIDType(binary=False), ForeignKey('user.id'))
    recipient_id = Column(UUIDType(binary=False), ForeignKey('user.id'))
    body = Column(db.String(140))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    read = Column(Boolean(), default=False)

    def __repr__(self):
        return f'<Message {self.body}>'