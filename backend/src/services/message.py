from typing import Sequence, List
from uuid import UUID

from sqlalchemy import select, insert, update, delete

from src.schemes.message import MessageInputScheme
from src.models import MessageModel, ChatModel
from src.config import db_session


async def create_message(
    user_id: UUID, chat_id: UUID, message: MessageInputScheme
) -> MessageModel:
    """Create new message"""

    async with db_session() as session:
        stmt = (
            insert(MessageModel)
            .values(user=user_id, chat=chat_id, **message.model_dump())
            .returning(MessageModel)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()


async def update_message(
    user_id: UUID, message_id: UUID, message: MessageInputScheme
) -> MessageModel:
    """Update message details"""

    async with db_session() as session:
        stmt = (
            update(MessageModel)
            .where(MessageModel.id == message_id)
            .where(MessageModel.user == user_id)
            .values(**message.model_dump())
            .returning(MessageModel)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()


async def delete_message(user_id: UUID, message_id: UUID) -> None:
    """Delete message"""

    async with db_session() as session:
        stmt = (
            delete(MessageModel)
            .where(MessageModel.id == message_id)
            .where(MessageModel.user == user_id)
        )
        await session.execute(stmt)
        await session.commit()


async def read_message(message: UUID) -> MessageModel:
    """Get specific message from chat"""

    async with db_session() as session:
        stmt = select(MessageModel).where(MessageModel.id == message)
        return await session.scalar(stmt)


async def read_messages(chat_id: UUID) -> Sequence[MessageModel]:
    """Get all chat messages"""

    async with db_session() as session:
        stmt = (
            select(MessageModel)
            .join(ChatModel, ChatModel.id == MessageModel.chat)
            .where(ChatModel.id == chat_id)
        )
        result = await session.scalars(stmt)
        return result.all()
