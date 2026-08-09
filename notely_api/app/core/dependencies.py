from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError

from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = HTTPBearer()


async def get_current_user(credentials=Depends(oauth2_scheme)) -> User:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token incorrect")
    user_id = payload.get("sub")
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur introuvable"
        )

    return user
