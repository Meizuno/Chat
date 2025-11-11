from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from src.utils import to_camel


class ChatScheme(BaseModel):
    """Base chat model"""

    id: UUID
    name: str
    is_muted: bool
    is_archived: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class ChatInputScheme(BaseModel):
    """Base model for create or update chat"""

    name: str
    is_muted: bool = False
    is_archived: bool = False

    class Config:
        alias_generator = to_camel
        populate_by_name = True
