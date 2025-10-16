# from sqlalchemy.ext.asyncio import AsyncSession
# from src.models import MessageModel


# async def create_message(session: AsyncSession, text: str) -> MessageModel:
#     """Create Message instance"""

#     message = MessageModel(text=text)
#     session.add(message)
#     await session.commit()
#     await session.refresh(message)
#     return message
