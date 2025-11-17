import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """Base user model"""

    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_2fa_enabled = Column(Boolean, default=False)
    otp_secret = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class ChatModel(Base):
    """Messenger chat model"""

    __tablename__ = "chat"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    is_muted = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class UserChatModel(Base):
    """Connection table between User and Chat"""

    __tablename__ = "user_chat"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE")
    )
    chat = Column(
        UUID(as_uuid=True), ForeignKey("chat.id", ondelete="CASCADE")
    )


class MessageModel(Base):
    """Message model"""

    __tablename__ = "message"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(TEXT)
    user = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE")
    )
    chat = Column(
        UUID(as_uuid=True), ForeignKey("chat.id", ondelete="CASCADE")
    )

    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
