from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.schemes import message as message_scheme
from src.services import message as message_service
from src.services.chat import check_chat_permission
from src.services.user import authenticated_user
from src.routers.chat import router as chat_router

router = APIRouter(
    prefix=f"{chat_router.prefix}/{{chat_id}}/message",
    tags=["message"],
    dependencies=[Depends(check_chat_permission)],
)


@router.get("")
async def read_messages(chat_id: UUID) -> List[message_scheme.MessageScheme]:
    """Read user chat messages"""

    messages = await message_service.read_messages(chat_id)
    return [
        message_scheme.MessageScheme.model_validate(message)
        for message in messages
    ]


@router.get("/{message_id}")
async def read_message(message_id: UUID) -> message_scheme.MessageScheme:
    """Read user chat message"""

    message = await message_service.read_message(message_id)
    return message_scheme.MessageScheme.model_validate(message)


@router.post("/")
async def create_message(
    chat_id: UUID,
    message: message_scheme.MessageInputScheme,
    user_id: UUID = Depends(authenticated_user),
) -> message_scheme.MessageScheme:
    """Create new message"""

    message = await message_service.create_message(user_id, chat_id, message)
    return message_scheme.MessageScheme.model_validate(message)


@router.put("/{message_id}")
async def update_chat(
    message_id: UUID,
    message: message_scheme.MessageInputScheme,
    user_id: UUID = Depends(authenticated_user),
) -> message_scheme.MessageScheme:
    """Create new chat"""

    chat = await message_service.update_message(user_id, message_id, message)
    return message_scheme.MessageScheme.model_validate(chat)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: UUID,
    user_id: UUID = Depends(authenticated_user),
) -> None:
    """Delete user chat"""

    await message_service.delete_message(user_id, message_id)
