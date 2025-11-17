import json
import uuid
from pathlib import Path
from src.logger import logger

FIXTURES_DIR = Path("fixtures")
FIXTURES_DIR.mkdir(exist_ok=True)

USERS_COUNT = 5
CHATS_PER_USER = 10
MESSAGES_PER_CHAT = 20

users = []
chats = []
user_chats = []
messages = []


# ---- USERS ----
for i in range(1, USERS_COUNT + 1):
    user_id = uuid.uuid4()
    users.append({
        "id": str(user_id),
        "first_name": f"User{i}",
        "last_name": "Test",
        "email": f"user{i}@example.com",
        "password": f"pass{i}"
    })

    # ---- CHATS ----
    for ci in range(1, CHATS_PER_USER + 1):
        chat_id = uuid.uuid4()
        chats.append({
            "id": str(chat_id),
            "name": f"Chat {i}-{ci}"
        })

        # relation
        user_chats.append({
            "id": str(uuid.uuid4()),
            "user": str(user_id),
            "chat": str(chat_id)
        })

        # ---- MESSAGES ----
        for mi in range(1, MESSAGES_PER_CHAT + 1):
            messages.append({
                "id": str(uuid.uuid4()),
                "text": f"Message {mi} in chat {i}-{ci}",
                "user": str(user_id),
                "chat": str(chat_id)
            })

# ---- WRITE FILES ----
(FIXTURES_DIR / "users.json").write_text(json.dumps(users, indent=2))
(FIXTURES_DIR / "chats.json").write_text(json.dumps(chats, indent=2))
(FIXTURES_DIR / "user_chats.json").write_text(json.dumps(user_chats, indent=2))
(FIXTURES_DIR / "messages.json").write_text(json.dumps(messages, indent=2))

logger.info("Fixtures generated!")
