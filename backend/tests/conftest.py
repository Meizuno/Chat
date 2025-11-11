from typing import Generator, Any

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.config import TOKEN_KEY, MAIL_SENDER
from src.schemes.user import AuthenticatedUser
from src.schemes.chat import ChatScheme


FIRST_NAME = "Name"
LAST_NAME = "Surname"
EMAIL = MAIL_SENDER
PASSWORD = "pass"


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    """Get FastAPI app"""

    with TestClient(app) as client:
        yield client


@pytest.fixture
def login(client: TestClient) -> tuple[str, str]:
    """Get access and refresh token"""

    response = client.post(
        "/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    return response.cookies[TOKEN_KEY], response.cookies[f"{TOKEN_KEY}_refresh"]


@pytest.fixture
def token(login: tuple[str, str]) -> str:
    """Get access token"""

    access_token, _ = login
    return access_token


@pytest.fixture
def refresh_token(login: tuple[str, str]) -> str:
    """Get refresh token"""

    _, refresh_user_token = login
    return refresh_user_token


@pytest.fixture
def user(client: TestClient, token: str) -> AuthenticatedUser:
    """Get authenticated user"""

    response = client.get("/user/me", cookies={TOKEN_KEY: token})
    return AuthenticatedUser.model_validate(response.json())


@pytest.fixture
def chat(client: TestClient, token: str) -> ChatScheme:
    """Get chat"""

    response = client.get("/chat", cookies={TOKEN_KEY: token})
    return ChatScheme.model_validate(response.json()[0])
