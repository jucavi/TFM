from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, String, Text
import uuid
from datetime import datetime
from app.helpers.date import local_time

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
    subject = Column(String(100))
    body = Column(Text())
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    read = Column(Boolean(), default=False)
    deleted = Column(Boolean(), default=False)

    @property
    def received(self):
        tn = datetime.utcnow()
        lt = local_time(self.timestamp)
        if (tn.day - self.timestamp.day) > 0:
            return lt.strftime('%d %b')
        return lt.strftime('%H:%M')

    @property
    def created(self):
        return local_time(self.timestamp)


    def __repr__(self):
        return f'<Message {self.subject}>'