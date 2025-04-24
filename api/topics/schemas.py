from pydantic import BaseModel, Field
from typing import List

class QuestionCreate(BaseModel):
    question_text: str

class TopicCreate(BaseModel):
    name: str
    description: str
    questions: List[QuestionCreate]

class TopicDelete(TopicCreate):
    pass
