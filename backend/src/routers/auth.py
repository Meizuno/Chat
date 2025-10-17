import io
from typing import Union, List
from uuid import UUID

import qrcode
from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.security import APIKeyCookie
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import get_pg_session
from src.schemes import user
from src.services import user as user_service
from src.config import TOKEN_KEY

router = APIRouter(prefix="/user", tags=["user"])
api_key_cookie = APIKeyCookie(name=TOKEN_KEY)


@router.post("/register")
async def register(
    response: Response,
    user: user.RegisterScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> user.UserResponse:
    """User registration"""

    user_instance = await user_service.create_user(session, user)
    user_service.set_auth_cookie(response, user_instance.username)
    return user.UserResponse.model_validate(user_instance)


@router.post("/login")
async def login(
    response: Response,
    credentials: user.LoginScheme,
    session: AsyncSession = Depends(get_pg_session),
) -> Union[user.UserResponse, user.OTPRequiredResponse]:
    """User registration"""

    user_instance = await user_service.user_login(session, credentials)
    if user_instance.is_2fa_enabled:
        return user.OTPRequiredResponse(
            otp_required=True, id=user_instance.id
        )

    user_service.set_auth_cookie(response, user_instance.id)
    return user.UserResponse.model_validate(user_instance)


@router.get("/me")
async def me(
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> user.UserResponse:
    """Read current user"""

    user_id = user_service.decode_token(token)
    return await user_service.get_user(session, user_id)


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
    verification: user.OTPValidateScheme,
    session: AsyncSession = Depends(get_pg_session),
):
    """Validate 2FA code and login"""

    user_instance = await user_service.validate_2fa(session, verification)
    user_service.set_auth_cookie(response, verification.username)
    return user.UserResponse.model_validate(user_instance)


@router.post("/logout")
async def logout(response: Response) -> None:
    """User logout"""

    user_service.delete_auth_cookie(response)


@router.get("/")
async def read_users(
    _: str = Depends(api_key_cookie),
    username_contains: str = "",
    session: AsyncSession = Depends(get_pg_session),
) -> List[user.UserSearchResponse]:
    """Get list of users whose usernames contain the given substring"""

    users = await user_service.search_users(session, username_contains)
    return [user.UserSearchResponse.model_validate(user) for user in users]


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    user_data: user.UserScheme,
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> user.UserResponse:
    """Update user information"""

    auth_user_id = user_service.decode_token(token)
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )

    user_instance = await user_service.update_user(session, user_id, user_data)
    return user.UserResponse.model_validate(user_instance)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    response: Response,
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> None:
    """Delete user"""

    auth_user_id = user_service.decode_token(token)
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )

    await user_service.delete_user(session, user_id)
    user_service.delete_auth_cookie(response)
