from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from src.config import DATABASE_URL, DEBUG


def get_pg_engine() -> AsyncEngine:
    """Create async PostgreSQL engine"""

    return create_async_engine(
        DATABASE_URL,
        echo=DEBUG,
        future=True,
        pool_pre_ping=True,
    )


async def get_pg_session():
    """Get PostgreSQL session"""

    async_session_maker = async_sessionmaker(
        bind=get_pg_engine(),
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with async_session_maker() as session:
        yield session
