from pydantic import BaseModel, Field
from uuid import UUID
from typing import List


class QuestionCreate(BaseModel):
    question_text: str

class QuestionOut(QuestionCreate):
    id: UUID
    class Config:
        from_attributes = True

class Topics(BaseModel):
    id: UUID
    name: str
    description: str


class TopicOut(Topics):
    questions: List[QuestionOut] = []

    class Config:
        from_attributes = True


class TopicCreate(BaseModel):
    name: str
    description: str
    questions: List[QuestionCreate]

