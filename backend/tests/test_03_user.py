from fastapi.testclient import TestClient
from src.config import TOKEN_KEY
from tests.conftest import (
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    PASSWORD,
)


def test_read_me(client: TestClient, token: str):
    """Test read self data"""

    response = client.get("/user/me", cookies={TOKEN_KEY: token})
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["firstName"] == FIRST_NAME
    assert response_json["lastName"] == LAST_NAME
    assert response_json["email"] == EMAIL


def test_search_user(client: TestClient, token: str):
    """Test search users"""

    response = client.get("/user", cookies={TOKEN_KEY: token})
    response_json = response.json()[0]

    assert response.status_code == 200
    assert response_json["firstName"] == FIRST_NAME
    assert response_json["lastName"] == LAST_NAME
    assert response_json["email"] == EMAIL


def test_update_user(client: TestClient, token: str):
    """Test update users"""

    response = client.put(
        "/user",
        json={
            "firstName": FIRST_NAME,
            "lastName": LAST_NAME,
        },
        cookies={TOKEN_KEY: token},
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["firstName"] == FIRST_NAME
    assert response_json["lastName"] == LAST_NAME
    assert response_json["email"] == EMAIL


def test_reset_password(client: TestClient, token: str):
    """Test update user password"""

    response = client.put(
        "/user/reset-password",
        json={"old": PASSWORD, "new": PASSWORD},
        cookies={TOKEN_KEY: token},
    )

    assert response.status_code == 204


def test_forgot_password(client: TestClient):
    """Test forgot user password"""

    response = client.post(
        "/user/forgot-password",
        json={"email": EMAIL, "redirectUrl": ""},
    )

    assert response.status_code == 204
