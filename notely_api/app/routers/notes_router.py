from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.note import Note
from app.models.user import User
from app.schemas.note_schema import NoteCreate, NoteOut, NoteUpdate

from app.services.llm_service import (
    LLMMalformedResponseError,
    LLMTimeoutError,
    LLMUnavailableError,
    generate_summary,
)
from datetime import datetime, timezone

router = APIRouter()


@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate, current_user: User = Depends(get_current_user)):
    note = await Note(
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
        source_url=payload.source_url,
    ).create()
    return note


@router.get("/notes", response_model=list[NoteOut])
async def list_notes(current_user: User = Depends(get_current_user)):
    return await Note.find(Note.user_id == current_user.id).to_list()


@router.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: str, current_user: User = Depends(get_current_user)):
    note = await Note.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note non trouvé")
    elif note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'êtes pas autorisé d'accéder à cette note"
        )
    else:
        return note


@router.put("/notes/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: str, payload: NoteUpdate, current_user: User = Depends(get_current_user)
):
    note = await Note.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note non trouvé")
    elif note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'êtes pas autorisé d'accéder à cette note"
        )
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    if payload.tags is not None:
        note.tags = payload.tags
    if payload.source_url is not None:
        note.source_url = payload.source_url
    await note.save()
    return note


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, current_user: User = Depends(get_current_user)):
    note = await Note.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note non trouvé")
    elif note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'êtes pas autorisé d'accéder à cette note"
        )
    await note.delete()


@router.post("/notes/{note_id}/summarize", response_model=NoteOut)
async def summarize_note(note_id: str, current_user: User = Depends(get_current_user)):
    note = await Note.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note non trouvé")
    elif note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous n'êtes pas autorisé d'accéder à ceette note"
        )

    try:
        summary = await generate_summary(note.content)
    except LLMUnavailableError:
        raise HTTPException(status_code=503, detail="Service LLM indisponible")
    except LLMTimeoutError:
        raise HTTPException(status_code=504, detail="Le LLM a mis trop de temps à répondre")
    except LLMMalformedResponseError:
        raise HTTPException(status_code=502, detail="Réponse du LLM invalide")

    note.summary_text = summary
    note.summary_model = settings.ollama_model
    note.summary_generated_at = datetime.now(timezone.utc)
    await note.save()
    return note
