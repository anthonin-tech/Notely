from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.db.mongodb import init_db
from app.models.user import User
from app.routers.auth_router import router as auth_router
from app.routers.notes_router import router as note_router
from app.routers.chatbot_router import router as chatbot_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Notely API", lifespan=lifespan)


@app.get("/health")
async def health():
    """Vérifie que l'API répond et que la connexion MongoDB fonctionne."""
    try:
        await User.find_one({})
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(note_router)
app.include_router(chatbot_router)
