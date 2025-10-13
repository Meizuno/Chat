from typing import Literal, Union
from pydantic import BaseModel, Field


class TextMessage(BaseModel):
    """Text model message schema"""

    type: Literal["text"]
    text: str = Field(..., min_length=1)


class Message(BaseModel):
    """Base message from client"""

    input: Union[TextMessage] = Field(discriminator="type")
