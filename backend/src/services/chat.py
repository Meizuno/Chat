from typing import Sequence, List
from uuid import UUID

from sqlalchemy import select, insert, update, delete, exists
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Request, Depends

from src.services.user import authenticated_user
from src.schemes.chat import ChatInputScheme
from src.models import ChatModel, UserChatModel
from src.config import db_session


async def create_chat(
    user_id: UUID, participants: List[UUID], chat: ChatInputScheme
) -> ChatModel:
    """Create new chat and link both users"""

    async with db_session() as session:
        try:
            stmt_chat = (
                insert(ChatModel)
                .values(**chat.model_dump())
                .returning(ChatModel)
            )
            result_chat = await session.execute(stmt_chat)
            chat_instance: ChatModel = result_chat.scalar_one()

            participants = [user_id, *participants]
            user_chat_values = [
                {"user": uid, "chat": chat_instance.id} for uid in participants
            ]

            stmt_user_chat = insert(UserChatModel).values(user_chat_values)
            await session.execute(stmt_user_chat)

            await session.commit()
            return chat_instance

        except IntegrityError as exc:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Chat creation failed (possibly duplicate)",
            ) from exc


async def update_chat(chat_id: UUID, chat: ChatInputScheme) -> ChatModel:
    """Update chat details"""

    async with db_session() as session:
        stmt = (
            update(ChatModel)
            .where(ChatModel.id == chat_id)
            .values(**chat.model_dump())
            .returning(ChatModel)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()


async def delete_chat(chat_id: UUID) -> None:
    """Delete chat (and cascade deletes user relations)"""

    async with db_session() as session:
        stmt = delete(ChatModel).where(ChatModel.id == chat_id)
        await session.execute(stmt)
        await session.commit()


async def read_chat(user_id: UUID, chat_id: UUID) -> ChatModel:
    """Get specific chat if user participates in it"""

    async with db_session() as session:
        stmt = (
            select(ChatModel)
            .join(UserChatModel, ChatModel.id == UserChatModel.chat)
            .where(UserChatModel.user == user_id)
            .where(ChatModel.id == chat_id)
        )
        return await session.scalar(stmt)


async def read_chats(user_id: UUID) -> Sequence[ChatModel]:
    """Get all chats for given user"""

    async with db_session() as session:
        stmt = (
            select(ChatModel)
            .join(UserChatModel, ChatModel.id == UserChatModel.chat)
            .where(UserChatModel.user == user_id)
        )
        result = await session.scalars(stmt)
        return result.all()


async def user_in_chat(user_id: UUID, chat_id: UUID) -> bool:
    """Check if user participates in chat"""

    async with db_session() as session:
        stmt = select(
            exists().where(
                UserChatModel.user == user_id, UserChatModel.chat == chat_id
            )
        )
        result = await session.scalar(stmt)
        return bool(result)


async def check_chat_permission(
    request: Request,
    user_id: UUID = Depends(authenticated_user)
) -> None:
    """Check user chat permission"""

    chat_id = request.path_params.get("chat_id")
    if chat_id is None:
        return

    chat_id = UUID(chat_id)
    has_access = await user_in_chat(user_id, chat_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this chat",
        )
