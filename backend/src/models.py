import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Uuid, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    """Message model"""

    __tablename__ = "message"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    text = Column(Text)

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class Chat(Base):
    """Messenger chat model"""

    __tablename__ = "chat"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
