from datetime import datetime
from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []
    source_url: Optional[str] = None


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    source_url: Optional[str] = None


class NoteOut(BaseModel):
    model_config = {"from_attributes": True}
    id: PydanticObjectId
    title: str
    content: str
    tags: list[str] = []
    source_url: Optional[str] = None
    summary_text: str | None
    created_at: datetime
    updated_at: datetime
