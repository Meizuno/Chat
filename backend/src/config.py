from environs import Env

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
TOKEN_EXPIRE = env.int("TOKEN_EXPIRE", 15)  # in minutes
REFRESH_TOKEN_EXPIRE = env.int("REFRESH_TOKEN_EXPIRE", 7)  # in days
BASE_URL = env.str("BASE_URL", "")
TOKEN_KEY = env.str("TOKEN_KEY", "session")
