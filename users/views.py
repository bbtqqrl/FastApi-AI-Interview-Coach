from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from auth.dependencies import get_current_user
from users import crud
from core.models import db_helper
from .schemas import Users, UserCreate, LogInUser
from auth.utils_jwt import create_access_token, validate_password
from .services import check_password_login
router = APIRouter(prefix='/users', tags=['users'])

@router.get("/", response_model=list[Users])
async def get_users(    
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_users(session=session)

@router.post("/", response_model=Users, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_user(session=session, user_in=user_in)



@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await check_password_login(
        username=form_data.username,
        password=form_data.password,
        session=session
    )

@router.get("/protected")
async def protected_route(user_data: dict = Depends(get_current_user)):
    return {"user": user_data}