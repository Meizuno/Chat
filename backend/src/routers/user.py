from typing import List, Annotated

from fastapi import APIRouter, Response, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import api_key_cookie
from src.services import get_pg_session
from src.schemes import user as user_scheme
from src.services import user as user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me")
async def me(
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
) -> user_scheme.AuthenticatedUser:
    """Read current user"""

    user_id = user_service.decode_token(token)
    user_instance = await user_service.get_user(session, user_id)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.get("/")
async def read_users(
    _: str = Depends(api_key_cookie),
    email_contains: str = "",
    session: AsyncSession = Depends(get_pg_session),
) -> List[user_scheme.UserScheme]:
    """Get list of users whose emails contain the given substring"""

    users = await user_service.search_users(session, email_contains)
    return [
        user_scheme.UserScheme.model_validate(user_instance)
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


@router.put("/reset-password")
async def reset_password(
    old: Annotated[str, Body()],
    new: Annotated[str, Body()],
    token: str = Depends(api_key_cookie),
    session: AsyncSession = Depends(get_pg_session),
):
    """Reset user password"""

    user_id = user_service.decode_token(token)
    await user_service.reset_password(session, user_id, old, new)


@router.post("/forgot-password")
async def forgot_password(
    email: Annotated[str, Body()],
    session: AsyncSession = Depends(get_pg_session),
) -> None:
    """Send mail to user for new password"""

    await user_service.forgot_password(session, email)
