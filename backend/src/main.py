from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from sqlalchemy import text

from src.config import BASE_URL, APP_TITLE
from src.routers import auth
from src.logger import logger
from src.models import Base
from src.services import (
    get_pg_engine,
    get_redis,
)


@asynccontextmanager
async def lifespan(app_span: FastAPI):
    """Lifespan FastAPI app"""

    app.state.redis = await get_redis()
    await app.state.redis.ping()
    logger.info("✅ Redis connection established")

    pg_engine = get_pg_engine()
    async with pg_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("✅ PostgreSQL connection established")

    async with pg_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ PostgreSQL migrated")

    yield

    await app_span.state.redis.close()
    logger.info("🛑 Application shutting down")


app = FastAPI(
    lifespan=lifespan,
    title=APP_TITLE,
    docs_url=f"{BASE_URL}/docs",
    redoc_url=f"{BASE_URL}/redoc",
    openapi_url=f"{BASE_URL}/openapi.json"
)


router = APIRouter(prefix=BASE_URL)
router.include_router(auth.router)
app.include_router(router)


@router.get("/")
def health():
    """Change if server is alive"""

    return "OK"


# @app.get("/stream")
# async def stream():
#     """Server Sent Action for new message"""

#     pubsub = app.state.redis.pubsub()
#     await pubsub.subscribe("chat")

#     async def event_stream():
#         try:
#             async for msg in pubsub.listen():
#                 if msg["type"] == "message":
#                     yield f"data: {msg['data']}\n\n"
#         finally:
#             await pubsub.unsubscribe("chat")
#             await pubsub.close()

#     return StreamingResponse(event_stream(), media_type="text/event-stream")


# @app.post("/message")
# async def send_message(
#     message: Message, session: AsyncSession = Depends(get_pg_session)
# ) -> MessageResponse:
#     """Post new message to chat"""

#     message_instance = await create_message(session, message.input.text)
#     message_response = MessageResponse.model_validate(message_instance)
#     await app.state.redis.publish("chat", message_response.model_dump_json())
#     return message_response
