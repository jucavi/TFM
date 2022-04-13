from app import db
from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, String, Text
import uuid
from datetime import datetime
from app.helpers.date import local_time

class Message(db.Model):
    __tablename__ = 'message'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index = True,
        default=uuid.uuid4
    )
    sender_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    subject = Column(String(100))
    body = Column(Text())
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    read = Column(Boolean(), default=False)
    deleted_by_recipient = Column(Boolean(), default=False)
    deleted_by_author = Column(Boolean(), default=False)

    @property
    def received(self):
        tn = datetime.utcnow()
        lt = local_time(self.timestamp)
        if (tn.day - self.timestamp.day) > 0:
            return lt.strftime('%b %d')
        return lt.strftime('%H:%M')

    @property
    def created(self):
        return local_time(self.timestamp)

    @property
    def date_time_format(self):
        return local_time(self.timestamp).strftime('%d %b %Y, %H:%M')

    def __repr__(self):
        return f'<Message {self.subject}>'