import io
from typing import Union

import qrcode
from fastapi import APIRouter, Response, Depends
from fastapi.security import APIKeyCookie
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import get_pg_session
from src.schemes.user import (
    UserScheme,
    UserResponse,
    LoginScheme,
    OTPValidateScheme,
    OTPRequiredResponse,
)
from src.services import user as user_service
from src.config import TOKEN_KEY

router = APIRouter(prefix="/user", tags=["user"])
api_key_cookie = APIKeyCookie(name=TOKEN_KEY)


@router.post("/register")
async def register(
    response: Response,
    user: UserScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> UserResponse:
    """User registration"""

    user_instance = await user_service.create_user(session, user)
    user_service.set_auth_cookie(response, user_instance.username)
    return UserResponse.model_validate(user_instance)


@router.post("/login")
async def login(
    response: Response,
    credentials: LoginScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> Union[UserResponse, OTPRequiredResponse]:
    """User registration"""

    user_instance = await user_service.user_login(session, credentials)
    if user_instance.is_2fa_enabled:
        return OTPRequiredResponse(
            otp_required=True, username=user_instance.username
        )

    user_service.set_auth_cookie(response, user_instance.username)
    return UserResponse.model_validate(user_instance)


@router.get("/me")
async def me(
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> UserResponse:
    """Read current user"""

    email = user_service.decode_token(token)
    return await user_service.get_user(session, email)


@router.post("/2fa")
async def enable_2fa(
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
):
    """Generate QR-code for enabling 2FA"""

    username = user_service.decode_token(token)
    otp_uri = await user_service.enable_2fa(session, username)

    qr = qrcode.make(otp_uri)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@router.post("/2fa/validate")
async def validate_2fa(
    response: Response,
    verification: OTPValidateScheme,
    session: AsyncSession = Depends(get_pg_session),
):
    """Validate 2FA code and login"""

    user_instance = await user_service.validate_2fa(session, verification)
    user_service.set_auth_cookie(response, verification.username)
    return UserResponse.model_validate(user_instance)
