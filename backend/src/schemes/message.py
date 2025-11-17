from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from src.utils import to_camel


class MessageScheme(BaseModel):
    """Base message model"""

    id: UUID
    text: str

    created_at: datetime
    updated_at: datetime

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class MessageInputScheme(BaseModel):
    """Base model for create or update message"""

    text: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
