from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body, status

from src.schemes import chat as chat_scheme
from src.services import chat as chat_service
from src.services.user import authenticated_user

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(chat_service.check_chat_permission)],
)


@router.get("/")
async def read_chats(
    user_id: UUID = Depends(authenticated_user)
) -> List[chat_scheme.ChatScheme]:
    """Read user chats"""

    chats = await chat_service.read_chats(user_id)
    return [chat_scheme.ChatScheme.model_validate(chat) for chat in chats]


@router.get("/{chat_id}")
async def read_chat(
    chat_id: UUID, user_id: UUID = Depends(authenticated_user)
) -> chat_scheme.ChatScheme:
    """Read user chat"""

    chat = await chat_service.read_chat(user_id, chat_id)
    return chat_scheme.ChatScheme.model_validate(chat)


@router.post("/")
async def create_chat(
    participants: Annotated[List[UUID], Body()],
    chat: chat_scheme.ChatInputScheme,
    user_id: UUID = Depends(authenticated_user)
) -> chat_scheme.ChatScheme:
    """Create new chat"""

    chat = await chat_service.create_chat(user_id, participants, chat)
    return chat_scheme.ChatScheme.model_validate(chat)


@router.put("/{chat_id}")
async def update_chat(
    chat_id: UUID, chat: chat_scheme.ChatInputScheme
) -> chat_scheme.ChatScheme:
    """Create new chat"""

    chat = await chat_service.update_chat(chat_id, chat)
    return chat_scheme.ChatScheme.model_validate(chat)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: UUID) -> None:
    """Delete user chat"""

    await chat_service.delete_chat(chat_id)
