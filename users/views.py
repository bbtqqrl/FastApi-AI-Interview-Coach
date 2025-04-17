from fastapi import APIRouter, Depends, HTTPException, status
from users import crud
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from .schemas import Users, UserCreate
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
