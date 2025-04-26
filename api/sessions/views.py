from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.sessions import crud, schemas 
from api.dependencies import get_current_user
from core.db_helper import db_helper
from services.redis_service import redis_service
from core.models.user import User

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# Старт сесії
@router.post("/start", response_model=schemas.SessionStartResponse)
async def start_session(
    data: schemas.SessionStartRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # Створюємо сесію
    session = await crud.create_session(
        db=db,
        user_id=current_user.id,
        topic_id=data.topic_id
    )

    # Отримуємо питання топіка
    questions = await crud.get_topic_questions(db=db, topic_id=data.topic_id)
    if not questions:
        raise HTTPException(status_code=400, detail="No questions available for this topic")

    # Кешуємо питання у Redis
    await redis_service.cache_questions(session_id=session.id, questions=questions)

    # Витягуємо перше питання (не видаляючи)
    first_question = await redis_service.get_first_question(session_id=session.id)

    return schemas.SessionStartResponse(
        session_id=session.id,
        first_question=first_question
    )

# Надіслати відповідь на питання
@router.post("/answer", response_model=schemas.NextQuestionResponse | schemas.SessionCompleteResponse)
async def submit_answer(
    data: schemas.AnswerSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # Дістаємо поточне питання (без LPOP)
    current_question = await redis_service.get_first_question(session_id=data.session_id)
    if not current_question:
        raise HTTPException(status_code=400, detail="No active question found")

    # Зберігаємо відповідь в БД
    await crud.add_user_answer(
        db=db,
        session_id=data.session_id,
        question=current_question,
        user_answer=data.answer
    )

    # Видаляємо це питання з Redis
    await redis_service.pop_next_question(session_id=data.session_id)

    # Перевіряємо, чи є ще питання
    has_questions = await redis_service.has_questions_left(session_id=data.session_id)

    if has_questions:
        next_question = await redis_service.get_first_question(session_id=data.session_id)
        return schemas.NextQuestionResponse(question=next_question)

    # Якщо питань більше нема — завершення сесії
    all_answers = await crud.get_session_answers(db=db, session_id=data.session_id)

    # Тут ти викликаєш ChatGPT для аналізу (тимчасово мок)
    results = [
        schemas.AnswerResult(
            question=ans.question,
            user_answer=ans.user_answer,
            ai_feedback="Good answer",  # мок
            score=8,  # мок
        )
        for ans in all_answers
    ]

    overall_score = sum(r.score for r in results) // len(results)
    overall_feedback = "Well done overall!"

    # Очищення кешу в Redis
    await redis_service.delete_questions(session_id=data.session_id)

    return schemas.SessionCompleteResponse(
        session_id=data.session_id,
        results=results,
        overall_score=overall_score,
        overall_feedback=overall_feedback,
    )
