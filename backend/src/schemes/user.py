from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from src.utils import to_camel


class RegisterScheme(BaseModel):
    """Base user model in application"""

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class AuthenticatedUser(BaseModel):
    """Model for authenticated user"""

    id: UUID
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    is_2fa_enabled: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class UserScheme(BaseModel):
    """Base user model in application"""

    id: UUID
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class UserUpdateScheme(BaseModel):
    """Model for user update"""

    first_name: str | None = None
    last_name: str | None = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OTPRequiredResponse(BaseModel):
    """Model for required OTP verification"""

    otp_required: bool
    user_id: UUID

    class Config:
        alias_generator = to_camel
        populate_by_name = True
