from pydantic import BaseModel


class ChatMessageIn(BaseModel):
    content: str


class ChatResponse(BaseModel):
    reply: str
