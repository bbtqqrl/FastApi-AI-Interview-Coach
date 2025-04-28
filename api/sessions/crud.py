from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.models import Session, UserResponse, Topic, Question

async def create_session(
    db: AsyncSession, 
    user_id: int, 
    topic_id: UUID
) -> Session:
    
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    session = Session(user_id=user_id, topic_id=topic_id, topic_title=topic.name)
    db.add(session)
    await db.commit()
    print(session)
    return session

async def add_user_answer(
    db: AsyncSession,
    session_id: UUID,
    question_id: UUID,
    question_text: str,
    user_answer: str,
) -> UserResponse:
    answer = UserResponse(
        session_id=session_id,
        question_id=question_id,
        question_text=question_text,
        answer_text=user_answer,
    )
    db.add(answer)
    await db.commit()
    return answer


async def get_session_answers(
    db: AsyncSession,
    session_id: int,
) -> list[UserResponse]:
    result = await db.execute(select(UserResponse).options(joinedload(UserResponse.question)).where(UserResponse.session_id == session_id))
    return result.scalars().all()

async def get_topic_questions(
    db: AsyncSession,
    topic_id: int
) -> list[str]:
    result = await db.execute(select(Question).where(Question.topic_id == topic_id))
    questions = result.scalars().all()
    return [{"id": str(q.id), "text": q.question_text} for q in questions]
