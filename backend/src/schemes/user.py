from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from src.utils import to_camel


class RegisterScheme(BaseModel):
    """Base user model in application"""

    first_name: str
    last_name: str
    username: str
    password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class LoginScheme(BaseModel):
    """Model for login"""

    username: str
    password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class AuthenticatedUser(BaseModel):
    """Model for authenticated user"""

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


class UserScheme(BaseModel):
    """Base user model in application"""

    id: UUID
    first_name: str
    last_name: str
    username: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserUpdateScheme(BaseModel):
    """Model for user update"""

    first_name: str
    last_name: str
    username: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserSearchResponse(BaseModel):
    """User model from search response"""

    id: UUID
    first_name: str
    last_name: str
    username: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class OTPValidateScheme(BaseModel):
    """Model for OTP verification"""

    user_id: UUID
    code: str = Field(..., min_length=6, max_length=6)

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
