from fastapi import Depends, HTTPException
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.exceptions import HTTPException
from auth.utils_jwt import create_access_token, validate_password

async def check_password_login(
    username: str,
    password: str,
    session: AsyncSession
):
    user = await crud.get_user_by_username(session, username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not validate_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return {
        "access_token": create_access_token({"sub": user.email}),
        "token_type": "bearer"
    }