from fastapi.testclient import TestClient
from src.config import TOKEN_KEY
from tests.conftest import (
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    PASSWORD,
)


def test_register(client: TestClient):
    """Test user registration"""

    response = client.post(
        "/auth/register",
        json={
            "firstName": FIRST_NAME,
            "lastName": LAST_NAME,
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    assert response.status_code == 201
    assert TOKEN_KEY in response.cookies
    assert f"{TOKEN_KEY}_refresh" in response.cookies


def test_conflict_register(client: TestClient):
    """Test conflict user registration"""

    response = client.post(
        "/auth/register",
        json={
            "firstName": FIRST_NAME,
            "lastName": LAST_NAME,
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    assert response.status_code == 409


def test_login(client: TestClient):
    """Test user login"""

    response = client.post(
        "/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    response_json = response.json()

    assert response.status_code == 200
    assert response_json["firstName"] == FIRST_NAME
    assert response_json["lastName"] == LAST_NAME
    assert response_json["email"] == EMAIL

    assert TOKEN_KEY in response.cookies
    assert f"{TOKEN_KEY}_refresh" in response.cookies


def test_refresh_token(client: TestClient, refresh_token: str):
    """Test refresh user token"""

    response = client.post(
        "/auth/refresh", cookies={f"{TOKEN_KEY}_refresh": refresh_token}
    )

    assert response.status_code == 204
    assert TOKEN_KEY in response.cookies
    assert f"{TOKEN_KEY}_refresh" in response.cookies


def test_logout(client: TestClient):
    """Test logout user"""

    response = client.post("/auth/logout")

    assert response.status_code == 204
    assert TOKEN_KEY not in response.cookies
    assert f"{TOKEN_KEY}_refresh" not in response.cookies
