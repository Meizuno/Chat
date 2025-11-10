import pytest
from fastapi.testclient import TestClient
from src.main import app

FIRST_NAME = "Name"
LAST_NAME = "Surname"
EMAIL = "user@example.com"
PASSWORD = "pass"


@pytest.fixture(scope="session", autouse=True)
async def setup():
    """Setup and cleanup for tests"""

    # Setup

    yield

    # Cleanup


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Get FastAPI app"""

    return TestClient(app)


# @pytest.fixture(scope="module")
# async def client() -> AsyncGenerator[AsyncClient, None]:
#     """Get FastAPI app"""

#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         yield ac
