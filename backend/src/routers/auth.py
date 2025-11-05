import io
from typing import Union, Annotated
from uuid import UUID

import qrcode
from pydantic import EmailStr
from fastapi import APIRouter, Response, Depends, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import api_key_cookie, refresh_api_key_cookie
from src.services import get_pg_session
from src.schemes import user as user_scheme
from src.services import user as user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    response: Response,
    user: user_scheme.RegisterScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> user_scheme.AuthenticatedUser:
    """User registration"""

    user_model = await user_service.create_user(session, user)
    user_service.set_auth_cookie(response, user_model.id)
    return user_scheme.AuthenticatedUser.model_validate(user_model)


@router.post("/login")
async def login(
    response: Response,
    email: Annotated[EmailStr, Body()],
    password: Annotated[str, Body()],
    session: AsyncSession = Depends(get_pg_session),
) -> Union[user_scheme.AuthenticatedUser, user_scheme.OTPRequiredResponse]:
    """User registration"""

    user_model = await user_service.user_login(session, email, password)
    if user_model.is_2fa_enabled:
        return user_scheme.OTPRequiredResponse(
            otp_required=True, user_id=user_model.id
        )

    user_service.set_auth_cookie(response, user_model.id)
    return user_scheme.AuthenticatedUser.model_validate(user_model)


@router.post("/refresh")
async def refresh_session(
    response: Response,
    refresh_token: str = Depends(refresh_api_key_cookie),
) -> None:
    """Refresh auth token"""

    user_id = user_service.decode_token(refresh_token)
    user_service.refresh_auth_cookie(response, user_id)


@router.post("/2fa")
async def enable_2fa(
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
):
    """Generate QR-code for enabling 2FA"""

    user_id = user_service.decode_token(token)
    otp_uri = await user_service.enable_2fa(session, user_id)

    qr = qrcode.make(otp_uri)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@router.post("/2fa/validate")
async def validate_2fa(
    response: Response,
    user_id: Annotated[UUID, Body()],
    code: Annotated[str, Body(min_length=6, max_length=6)],
    session: AsyncSession = Depends(get_pg_session),
):
    """Validate 2FA code and login"""

    user_model = await user_service.validate_2fa(session, user_id, code)
    user_service.set_auth_cookie(response, user_id)
    return user_scheme.AuthenticatedUser.model_validate(user_model)


@router.post("/logout")
async def logout(response: Response) -> None:
    """User logout"""

    user_service.delete_auth_cookie(response)
