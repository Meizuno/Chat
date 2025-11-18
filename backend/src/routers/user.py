from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Response, Depends, Body, status

from src.config import api_key_cookie
from src.schemes import user as user_scheme
from src.services import user as user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me")
async def me(
    user_id: UUID = Depends(user_service.authenticated_user),
) -> user_scheme.AuthenticatedUser:
    """Read current user"""

    user_instance = await user_service.get_user(user_id)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.get("/")
async def read_users(
    _: UUID = Depends(user_service.authenticated_user),
    email_contains: str = "",
) -> List[user_scheme.UserScheme]:
    """Get list of users whose emails contain the given substring"""

    users = await user_service.search_users(email_contains)
    return [
        user_scheme.UserScheme.model_validate(user_instance)
        for user_instance in users
    ]


@router.put("/")
async def update_user(
    user_data: user_scheme.UserUpdateScheme,
    user_id: UUID = Depends(user_service.authenticated_user),
) -> user_scheme.AuthenticatedUser:
    """Update user information"""

    user_instance = await user_service.update_user(user_id, user_data)
    return user_scheme.AuthenticatedUser.model_validate(user_instance)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    response: Response, user_id: UUID = Depends(user_service.authenticated_user)
) -> None:
    """Delete user"""

    await user_service.delete_user(user_id)
    user_service.delete_auth_cookie(response)


@router.put("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    old: Annotated[str, Body()],
    new: Annotated[str, Body()],
    user_id: UUID = Depends(user_service.authenticated_user),
) -> None:
    """Reset user password"""

    await user_service.reset_password(user_id, old, new)


@router.post("/forgot-password", status_code=status.HTTP_204_NO_CONTENT)
async def forgot_password(
    email: Annotated[str, Body()],
    redirect_url: Annotated[str, Body(alias="redirectUrl")],
) -> None:
    """Send mail to user for new password"""

    await user_service.forgot_password(email, redirect_url)
