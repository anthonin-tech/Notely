from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models.conversation import ChatMessage, Conversation
from app.models.user import User
from app.schemas.chat_schema import ChatMessageIn, ChatResponse
from app.services.llm_service import (
    LLMMalformedResponseError,
    LLMTimeoutError,
    LLMUnavailableError,
    generate_chat_reply,
)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatMessageIn, current_user: User = Depends(get_current_user)):
    conversation = await Conversation.find_one(Conversation.user_id == current_user.id)
    if conversation is None:
        conversation = Conversation(user_id=current_user.id)
    new_message = ChatMessage(role="user", content=payload.content)
    conversation.messages.append(new_message)
    messages_llm = []
    for msg in conversation.messages:
        message_dict = {"role": msg.role, "content": msg.content}
        messages_llm.append(message_dict)
    try:
        reply = await generate_chat_reply(messages_llm)
    except LLMUnavailableError:
        raise HTTPException(status_code=503, detail="Service LLM indisponible")
    except LLMTimeoutError:
        raise HTTPException(status_code=504, detail="Le LLM a mis trop de temps à répondre")
    except LLMMalformedResponseError:
        raise HTTPException(status_code=502, detail="Réponse du LLM invalide")
    conversation.messages.append(ChatMessage(role="assistant", content=reply))
    await conversation.save()
    return ChatResponse(reply=reply)
