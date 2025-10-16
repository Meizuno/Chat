from uuid import UUID
from typing import Literal, Union
from datetime import datetime
from pydantic import BaseModel, Field
from src.utils import to_camel


class UserScheme(BaseModel):
    """Base user model in application"""

    first_name: str
    last_name: str
    username: str
    password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserResponse(BaseModel):
    """User model from response"""

    id: UUID
    first_name: str
    last_name: str
    username: str
    is_2fa_enabled: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class TextMessageScheme(BaseModel):
    """Text model message schema"""

    type: Literal["text"]
    text: str = Field(..., min_length=1)

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class MessageScheme(BaseModel):
    """Base message from client"""

    input: Union[TextMessageScheme] = Field(discriminator="type")

    class Config:
        alias_generator = to_camel
        populate_by_name = True


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


class LoginScheme(BaseModel):
    """Model for login"""

    username: str
    password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OTPValidateScheme(BaseModel):
    """Model for OTP verification"""

    username: str
    code: str = Field(..., min_length=6, max_length=6)

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OTPRequiredResponse(BaseModel):
    """Model for required OTP verification"""

    otp_required: bool
    username: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
