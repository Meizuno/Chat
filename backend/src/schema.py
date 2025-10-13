from uuid import UUID
from typing import Literal, Union
from datetime import datetime
from pydantic import BaseModel, Field


class TextMessage(BaseModel):
    """Text model message schema"""

    type: Literal["text"]
    text: str = Field(..., min_length=1)


class Message(BaseModel):
    """Base message from client"""

    input: Union[TextMessage] = Field(discriminator="type")


class MessageResponse(BaseModel):
    """Base message response"""

    id: UUID
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
