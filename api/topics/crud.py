from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import UUID, insert
from core.models.topic import Topic
from core.models.question import Question
from .schemas import TopicCreate

async def create_topic(db: AsyncSession, topic_data: TopicCreate):
    new_topic = Topic(name=topic_data.name, description=topic_data.description)
    db.add(new_topic)
    await db.flush()

    questions = [
        Question(question_text=q.question_text, topic_id=new_topic.id) for q in topic_data.questions
    ]
    db.add_all(questions)
    await db.commit()
    await db.refresh(new_topic)
    return new_topic

async def delete_topic(db: AsyncSession, topic_id: UUID):
    result = await db.execute(select(Topic).where(Topic.id == topic_id))
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    await db.delete(topic)
    await db.commit()


async def get_topic(db: AsyncSession, topic_name: str) -> Topic:
    result = await db.execute(select(Topic).where(Topic.name == topic_name).options(selectinload(Topic.questions)))
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    return topic

async def get_all_topic(db: AsyncSession) -> list[Topic]:
    result = await db.execute(select(Topic))
    topics = result.scalars().all()
    return topics


