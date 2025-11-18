import io
from typing import Union, Annotated
from uuid import UUID

import qrcode
from pydantic import EmailStr
from fastapi import APIRouter, Response, Depends, Body, status
from fastapi.responses import StreamingResponse

from src.config import api_key_cookie, refresh_api_key_cookie
from src.schemes import user as user_scheme
from src.services import user as user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    response: Response,
    user: user_scheme.RegisterScheme,
) -> user_scheme.AuthenticatedUser:
    """User registration"""

    user_model = await user_service.create_user(user)
    user_service.set_auth_cookie(response, user_model.id)
    return user_scheme.AuthenticatedUser.model_validate(user_model)


@router.post("/login")
async def login(
    response: Response,
    email: Annotated[EmailStr, Body()],
    password: Annotated[str, Body()],
) -> Union[user_scheme.AuthenticatedUser, user_scheme.OTPRequiredResponse]:
    """User registration"""

    user_model = await user_service.user_login(email, password)
    if user_model.is_2fa_enabled:
        return user_scheme.OTPRequiredResponse(
            otp_required=True, user_id=user_model.id
        )

    user_service.set_auth_cookie(response, user_model.id)
    return user_scheme.AuthenticatedUser.model_validate(user_model)


@router.post("/refresh", status_code=status.HTTP_204_NO_CONTENT)
async def refresh_session(
    response: Response,
    user_id: UUID = Depends(user_service.refresh_authenticated_user),
) -> None:
    """Refresh auth token"""

    user_service.refresh_auth_cookie(response, user_id)


@router.post("/2fa")
async def enable_2fa(
    user_id: UUID = Depends(user_service.authenticated_user)
):
    """Generate QR-code for enabling 2FA"""

    otp_uri = await user_service.enable_2fa(user_id)

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
):
    """Validate 2FA code and login"""

    user_model = await user_service.validate_2fa(user_id, code)
    user_service.set_auth_cookie(response, user_id)
    return user_scheme.AuthenticatedUser.model_validate(user_model)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    """User logout"""

    user_service.delete_auth_cookie(response)
