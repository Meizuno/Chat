import json
from pathlib import Path
from src.config import db_session
from src.models import UserModel, ChatModel, UserChatModel, MessageModel
from src.logger import logger

FIXTURES_DIR = Path("fixtures")

async def seed():
    async with db_session() as session:
        users = json.loads((FIXTURES_DIR / "users.json").read_text())
        chats = json.loads((FIXTURES_DIR / "chats.json").read_text())
        user_chats = json.loads((FIXTURES_DIR / "user_chats.json").read_text())
        messages = json.loads((FIXTURES_DIR / "messages.json").read_text())

        for u in users:
            session.add(UserModel(**u))
        
        await session.commit()

        for c in chats:
            session.add(ChatModel(**c))

        for uc in user_chats:
            session.add(UserChatModel(**uc))

        for m in messages:
            session.add(MessageModel(**m))

        await session.commit()

    logger.info("Database seeded successfully!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
