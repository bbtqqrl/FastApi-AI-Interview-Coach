from uuid import UUID
from pydantic import BaseModel
from typing import List

class SessionResponse(BaseModel):
    session_id: UUID
    question_id: UUID
    question_text: str

class AnswerSubmitRequest(BaseModel):
    answer: str

class AnswerResult(BaseModel):
    question_id: UUID
    question_text: str
    user_answer: str
    ai_feedback: str
    score: int

class SessionCompleteResponse(BaseModel):
    session_id: UUID
    results: List[AnswerResult]
    overall_score: int
    overall_feedback: str

