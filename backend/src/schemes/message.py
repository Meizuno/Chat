from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from src.utils import to_camel


class MessageResponse(BaseModel):
    """Base message response"""

    id: UUID
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
