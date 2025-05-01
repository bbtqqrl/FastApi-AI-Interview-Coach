import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.sessions import crud, schemas 
from api.dependencies import get_current_user
from core.db_helper import db_helper
from services.redis_service import redis_service
from core.models.user import User
from . import session_service
router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/{topic_id}", response_model=schemas.SessionId)
async def start_session(
    topic_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    session = await crud.create_session(
        db=db,
        user_id=current_user["id"],
        topic_id=topic_id
    )

    questions = await crud.get_topic_questions(db=db, topic_id=topic_id)
    if not questions:
        raise HTTPException(status_code=400, detail="No questions available for this topic")
    await redis_service.cache_questions(session_id=session.id, questions=questions)

    return schemas.SessionId(
        session_id=session.id,
    )

@router.post("/get-question/{session_id}", response_model=schemas.SessionResponse)
async def send_question(
    session_id: UUID,
    _: User = Depends(get_current_user),
):
    current_question = await redis_service.get_current_question(session_id)
    if current_question:
        return schemas.SessionResponse(session_id=session_id, question_id=current_question["id"], question_text= current_question["text"])
        
    question = await redis_service.pop_next_question(session_id)
    if not question:
        raise HTTPException(status_code=404, detail="No questions left.")

    await redis_service.set_current_question(session_id, question)
    return schemas.SessionResponse(session_id=session_id, question_id=question["id"], question_text= question["text"])

@router.post("/submit-answer/{session_id}", response_model=schemas.AnswerSubmitRequest | schemas.SessionCompleteResponse)
async def send_answer(
    session_id: UUID,
    data: schemas.AnswerRequest,
    _: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    current_question = await redis_service.get_current_question(session_id)
    print(f"send_answer current_question - {current_question}")

    if not current_question:
        raise HTTPException(status_code=400, detail="No question issued. Please request a question before submitting an answer." )
    
    await session_service.process_single_answer(db=db, session_id=session_id, current_question=current_question, user_answer=data.answer)
    has_questions = await redis_service.has_questions_left(session_id=session_id)

    if has_questions:
        return schemas.AnswerSubmitRequest(result={"message": "Answer submitted successfully. Please request the next question."})

    else:
        return await session_service.complete_session(db=db, session_id=session_id)


