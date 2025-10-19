import io
from typing import Union, List

import qrcode
from fastapi import APIRouter, Response, Depends
from fastapi.security import APIKeyCookie
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import get_pg_session
from src.schemes import user as user_scheme
from src.services import user as user_service
from src.config import TOKEN_KEY

router = APIRouter(prefix="/user", tags=["user"])
api_key_cookie = APIKeyCookie(name=TOKEN_KEY)
refresh_api_key_cookie = APIKeyCookie(name=f"{TOKEN_KEY}_refresh")


@router.post("/register")
async def register(
    response: Response,
    user: user_scheme.RegisterScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> user_scheme.AuthenticatedUser:
    """User registration"""

    user_instance = await user_service.create_user(session, user)
    user_service.set_auth_cookie(response, user_instance.username)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.post("/login")
async def login(
    response: Response,
    credentials: user_scheme.LoginScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> Union[user_scheme.AuthenticatedUser, user_scheme.OTPRequiredResponse]:
    """User registration"""

    user_instance = await user_service.user_login(session, credentials)
    if user_instance.is_2fa_enabled:
        return user_scheme.OTPRequiredResponse(
            otp_required=True, user_id=user_instance.id
        )

    user_service.set_auth_cookie(response, user_instance.id)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.post("/refresh")
async def refresh_session(
    response: Response,
    refresh_token: str = Depends(refresh_api_key_cookie),
) -> None:
    """Refresh auth token"""

    user_id = user_service.decode_token(refresh_token)
    user_service.refresh_auth_cookie(response, user_id)


@router.get("/me")
async def me(
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> user_scheme.AuthenticatedUser:
    """Read current user"""

    user_id = user_service.decode_token(token)
    user_instance = await user_service.get_user(session, user_id)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


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
    verification: user_scheme.OTPValidateScheme,
    session: AsyncSession = Depends(get_pg_session),
):
    """Validate 2FA code and login"""

    user_instance = await user_service.validate_2fa(session, verification)
    user_service.set_auth_cookie(response, verification.user_id)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.post("/logout")
async def logout(response: Response) -> None:
    """User logout"""

    user_service.delete_auth_cookie(response)


@router.get("/")
async def read_users(
    _: str = Depends(api_key_cookie),
    username_contains: str = "",
    session: AsyncSession = Depends(get_pg_session),
) -> List[user_scheme.UserSearchResponse]:
    """Get list of users whose usernames contain the given substring"""

    users = await user_service.search_users(session, username_contains)
    return [
        user_scheme.UserSearchResponse.model_validate(user_instance)
        for user_instance in users
    ]


@router.put("/")
async def update_user(
    user_data: user_scheme.UserUpdateScheme,
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> user_scheme.AuthenticatedUser:
    """Update user information"""

    auth_user_id = user_service.decode_token(token)
    user_instance = await user_service.update_user(
        session, auth_user_id, user_data
    )
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.delete("/")
async def delete_user(
    response: Response,
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> None:
    """Delete user"""

    auth_user_id = user_service.decode_token(token)
    await user_service.delete_user(session, auth_user_id)
    user_service.delete_auth_cookie(response)
