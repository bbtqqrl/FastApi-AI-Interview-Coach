from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class QuestionOut(BaseModel):
    id: UUID
    question_text: str

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


class QuestionCreate(BaseModel):
    question_text: str

class TopicCreate(BaseModel):
    name: str
    description: str
    questions: List[QuestionCreate]

