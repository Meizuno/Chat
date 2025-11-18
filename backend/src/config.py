from environs import Env
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
import redis

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)
RELEASE = not DEBUG

# Redis configuration
REDIS_URL = env.str("REDIS_URL", "redis://localhost/0")
redis_client = redis.from_url(
    REDIS_URL, encoding="utf-8", decode_responses=True
)

# Database configuration
DATABASE_URL = env.str(
    "DATABASE_URL", "postgresql+asyncpg://user:1234@localhost/chat"
)
engine = create_async_engine(DATABASE_URL, echo=DEBUG)
db_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Application configuration
BASE_URL = env.str("BASE_URL", "")
APP_TITLE = env.str("APP_TITLE", "ChatApplication")
SECRET_KEY = env.str("SECRET_KEY", "test")
ALGORITHM = env.str("ALGORITHM", "HS256")

# Authorization configuration
TOKEN_EXPIRE = env.int("TOKEN_EXPIRE", 900)  # in seconds
REFRESH_TOKEN_EXPIRE = env.int("REFRESH_TOKEN_EXPIRE", 21600)  # in seconds
TOKEN_KEY = env.str("TOKEN_KEY", "session")
api_key_cookie = APIKeyCookie(name=TOKEN_KEY)
refresh_api_key_cookie = APIKeyCookie(name=f"{TOKEN_KEY}_refresh")

# Mail configuration
MAIL_SENDER = env.str("MAIL_SENDER", "")
MAIL_API_KEY = env.str("MAIL_API_KEY", "")
