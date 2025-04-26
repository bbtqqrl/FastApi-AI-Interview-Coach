from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from . import crud, schemas
from api.dependencies import verify_admin
from core.db_helper import db_helper
from .schemas import TopicOut, Topics

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/", response_model=list[Topics], status_code=status.HTTP_200_OK)
async def get_all_topics_view(
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ):
    return await crud.get_all_topic(db)

@router.get("/{topic_name}", response_model=TopicOut, status_code=status.HTTP_200_OK)
async def get_topic_view(
    topic_name: str,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ):
    return await crud.get_topic(db, topic_name)

@router.post("/create", response_model=TopicOut , status_code=status.HTTP_201_CREATED)
async def create_topic_view(
    topic: schemas.TopicCreate, 
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    is_admin: bool = Depends(verify_admin)
    ):
    return await crud.create_topic(db, topic)

@router.delete("/delete/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic_view(
    topic_id: UUID,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    is_admin: bool = Depends(verify_admin)
    ):
    return await crud.delete_topic(db, topic_id)

