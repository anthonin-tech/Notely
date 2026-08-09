from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Note(Document):
    user_id: Indexed(PydanticObjectId)
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    source_url: Optional[str] = None
    summary_text: Optional[str] = None
    summary_model: Optional[str] = None
    summary_generated_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "notes"
