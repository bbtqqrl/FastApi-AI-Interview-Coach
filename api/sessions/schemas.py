from uuid import UUID
from pydantic import BaseModel
from typing import List

class SessionId(BaseModel):
    session_id: UUID

class SessionResponse(SessionId):
    question_id: UUID
    question_text: str

class AnswerRequest(BaseModel):
    session_id: UUID
    answer: str

class AnswerSubmitRequest(BaseModel):
    result: str | Exception

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

