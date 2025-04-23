from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
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
