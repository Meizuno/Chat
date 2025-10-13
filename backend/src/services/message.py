from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Message


async def create_message(session: AsyncSession, text: str) -> Message:
    """Create Message instance"""

    message = Message(text=text)
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message
