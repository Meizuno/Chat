import pytest
from fastapi.testclient import TestClient
# from httpx import AsyncClient
from sqlalchemy import text

from src.services import (
    get_pg_engine,
    get_redis,
)


def test_health(client: TestClient):
    """Test app health"""

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "OK"


# @pytest.mark.anyio
# async def test_redis_connection():
#     """Test redis connection"""

#     r = await get_redis()
#     await r.ping()
#     await r.close()


# @pytest.mark.anyio
# async def test_db_connection():
#     """Test database connection"""

#     pg_engine = get_pg_engine()
#     async with pg_engine.connect() as conn:
#         await conn.execute(text("SELECT 1"))
