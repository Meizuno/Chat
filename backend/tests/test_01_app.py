from fastapi.testclient import TestClient


def test_health(client: TestClient):
    """Test app health"""

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "OK"
