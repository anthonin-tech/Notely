from fastapi import APIRouter, HTTPException, status, Depends

from app.core.security import create_access_token, hash_password, verify_password
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth_schema import Token, UserLogin, UserOut, UserRegister

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    registed = await User.find_one(User.email == payload.email)
    if registed:
        raise HTTPException(status_code=409, detail="Email déjà utilisé")
    hashed_password = hash_password(payload.password)
    user = await User(email=payload.email, password_hash=hashed_password).create()
    return user


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    user = await User.find_one(User.email == payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="email ou mot de passe incorrect")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
