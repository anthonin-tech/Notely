from datetime import datetime, timezone

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Conversation(Document):
    user_id: Indexed(PydanticObjectId)
    messages: list[ChatMessage] = Field(default_factory=list)

    class Settings:
        name = "conversations"
