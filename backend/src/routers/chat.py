from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Response, Depends, Body, status

from src.config import api_key_cookie
from src.schemes import chat as chat_scheme
from src.services import chat as chat_service
from src.services import user as user_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
async def read_chats(
    token: str = Depends(api_key_cookie),
) -> List[chat_scheme.ChatScheme]:
    """Read user chats"""

    user_id = user_service.decode_token(token)
    chats = await chat_service.read_chats(user_id)
    return [chat_scheme.ChatScheme.model_validate(chat) for chat in chats]


@router.get("/{chat_id}")
async def read_chats(
    chat_id: UUID, token: str = Depends(api_key_cookie)
) -> chat_scheme.ChatScheme:
    """Read user chat"""

    user_id = user_service.decode_token(token)
    chat = await chat_service.read_chat(user_id, chat_id)
    return chat_scheme.ChatScheme.model_validate(chat)


@router.post("/")
async def create_chat(
    participants: Annotated[List[UUID], Body()],
    chat: chat_scheme.ChatInputScheme,
    token: str = Depends(api_key_cookie),
) -> chat_scheme.ChatScheme:
    """Create new chat"""

    user_id = user_service.decode_token(token)
    chat = await chat_service.create_chat(user_id, participants, chat)
    return chat_scheme.ChatScheme.model_validate(chat)


@router.put("/{chat_id}")
async def update_chat(
    chat_id: UUID,
    chat: chat_scheme.ChatInputScheme,
    token: str = Depends(api_key_cookie),
) -> chat_scheme.ChatScheme:
    """Create new chat"""

    user_id = user_service.decode_token(token)
    chat = await chat_service.update_chat(chat_id, chat)
    return chat_scheme.ChatScheme.model_validate(chat)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: UUID, token: str = Depends(api_key_cookie)
) -> None:
    """Delete user chat"""

    await chat_service.delete_chat(chat_id)
