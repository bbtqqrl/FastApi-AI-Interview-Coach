from pydantic import BaseModel
from typing import List

class SessionStartRequest(BaseModel):
    topic_id: int

class SessionResponse(BaseModel):
    session_id: int
    question: str

class AnswerSubmitRequest(BaseModel):
    session_id: int
    answer: str

class AnswerResult(BaseModel):
    question: str
    user_answer: str
    ai_feedback: str
    score: int

class SessionCompleteResponse(BaseModel):
    session_id: int
    results: List[AnswerResult]
    overall_score: int
    overall_feedback: str

