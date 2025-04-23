from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils_jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        return payload  
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
