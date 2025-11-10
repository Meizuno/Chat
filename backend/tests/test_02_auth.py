from fastapi.testclient import TestClient
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

    assert response.status_code == 200


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
