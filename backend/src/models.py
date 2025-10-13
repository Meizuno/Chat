from datetime import datetime, timezone
from sqlalchemy import Column, Uuid, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Chat(Base):
    """Messenger chat model"""

    __tablename__ = "chat"

    id = Column(Uuid, primary_key=True)
    text = Column(Text)

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
