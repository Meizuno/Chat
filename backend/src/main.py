from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema import Message
from src.logger import logger
from src.models import Base
from src.services.pg import get_pg_engine, get_pg_session
from src.services.redis import get_redis


@asynccontextmanager
async def lifespan(app_span: FastAPI):
    """Lifespan FastAPI app"""

    redis = await get_redis()
    await redis.ping()
    logger.info("✅ Redis connection established")

    pg_engine = get_pg_engine()
    async with pg_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("✅ PostgreSQL connection established")

    async with app_span.state.pg.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ PostgreSQL migrated")

    yield

    await app_span.state.redis.close()
    logger.info("🛑 Application shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def health():
    """Change if server is alive"""

    return "OK"


@app.get("/stream")
async def stream():
    """Server Sent Action for new message"""

    pubsub = app.state.redis.pubsub()
    await pubsub.subscribe("chat")

    async def event_stream():
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    yield f"data: {message['data']}\n\n"
        finally:
            await pubsub.unsubscribe("chat")
            await pubsub.close()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/send")
async def send_message(
    message: Message, session: AsyncSession = Depends(get_pg_session)
):
    """Post new message to chat"""

    message = message.model_dump_json()
    await app.state.redis.publish("chat", message)
    return {"status": "ok"}
