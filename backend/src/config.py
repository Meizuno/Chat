from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", True)
REDIS_URL = env.str("REDIS_URL", "redis://localhost/1")
POSTGRES_URL = env.str("POSTGRES_URL", "postgresql+asyncpg://user:1234@localhost/chat")
