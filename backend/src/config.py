from environs import Env
from fastapi.security import APIKeyCookie

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", True)
REDIS_URL = env.str("REDIS_URL", "redis://localhost/1")
POSTGRES_URL = env.str(
    "POSTGRES_URL", "postgresql+asyncpg://user:1234@localhost/chat"
)

APP_TITLE = env.str("APP_TITLE", "ChatApplication")
SECRET_KEY = env.str("SECRET_KEY", "test")
ALGORITHM = env.str("ALGORITHM", "HS256")
TOKEN_EXPIRE = env.int("TOKEN_EXPIRE", 900)  # in seconds
REFRESH_TOKEN_EXPIRE = env.int("REFRESH_TOKEN_EXPIRE", 21600)  # in seconds
BASE_URL = env.str("BASE_URL", "")
TOKEN_KEY = env.str("TOKEN_KEY", "session")

MAIL_SENDER = env.str("MAIL_SENDER", "")
MAIL_API_KEY = env.str("MAIL_API_KEY", "")
APP_UI_URL = env.str("APP_UI_URL", "http://localhost:3000")

api_key_cookie = APIKeyCookie(name=TOKEN_KEY)
refresh_api_key_cookie = APIKeyCookie(name=f"{TOKEN_KEY}_refresh")
