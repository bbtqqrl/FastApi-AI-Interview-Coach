from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from core.models import db_helper


router = APIRouter(prefix="/topics", tags=["Topics"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_topic_view(topic: schemas.TopicCreate, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_topic(db, topic)

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic_view(topic_id: str, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.delete_topic(db, topic_id)