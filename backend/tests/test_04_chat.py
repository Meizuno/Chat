from fastapi.testclient import TestClient
from src.schemes.chat import ChatScheme
from src.config import TOKEN_KEY


def test_create_chat(client: TestClient, token: str):
    """Test create user chat"""

    response = client.post(
        "/chat",
        json={
            "participants": [],
            "chat": {
                "name": "Chat name",
            },
        },
        cookies={TOKEN_KEY: token},
    )

    assert response.status_code == 200


def test_update_chat(client: TestClient, token: str, chat: ChatScheme):
    """Test update user chat"""

    response = client.put(
        f"/chat/{chat.id}",
        json={
            "name": "Chat updated name",
        },
        cookies={TOKEN_KEY: token},
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["id"] == str(chat.id)
    assert response_json["name"] == "Chat updated name"


def test_read_chat(client: TestClient, token: str, chat: ChatScheme):
    """Test read chat"""

    response = client.get(f"/chat/{chat.id}", cookies={TOKEN_KEY: token})

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["id"] == str(chat.id)
    assert response_json["name"] == "Chat updated name"


def test_read_chats(client: TestClient, token: str, chat: ChatScheme):
    """Test read chats"""

    response = client.get("/chat", cookies={TOKEN_KEY: token})

    response_json = response.json()[0]
    assert response.status_code == 200
    assert response_json["id"] == str(chat.id)
    assert response_json["name"] == "Chat updated name"


def test_delete_chat(client: TestClient, token: str, chat: ChatScheme):
    """Test delete chat"""

    response = client.delete(f"/chat/{chat.id}", cookies={TOKEN_KEY: token})
    assert response.status_code == 204
