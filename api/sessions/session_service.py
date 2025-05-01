import json
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from api.sessions import crud, schemas 
from services.redis_service import redis_service
from services import ai_service

async def process_single_answer(
    db: AsyncSession,
    session_id: UUID,
    current_question: dict,
    user_answer: str
) -> dict:
    data_for_ai = f"Question {current_question['text']}. Answer {user_answer}"
    ai_analyze = await ai_service.get_ai_analyze(
        data=data_for_ai,
        prompt=ai_service.PROMPTS["single_answer"]
    )

    await crud.add_user_answer(
        db=db,
        session_id=session_id,
        question_id=current_question["id"],
        question_text=current_question["text"],
        user_answer=user_answer,
        ai_feedback=ai_analyze['verdict'],
        score=ai_analyze['score']
    )

    await redis_service.clear_current_question(str(session_id))
    return ai_analyze


async def complete_session(db: AsyncSession, session_id: UUID) -> schemas.SessionCompleteResponse:
    all_answers = await crud.get_session_answers(db=db, session_id=session_id)

    results = [
        schemas.AnswerResult(
            question_id=ans.question_id,
            question_text=ans.question_text,
            user_answer=ans.answer_text,
            ai_feedback=ans.ai_feedback,
            score=ans.score,
        )
        for ans in all_answers
    ]

    data_for_ai = [{"question": res.question_text, "answer": res.user_answer} for res in results]
    json_results = json.dumps(data_for_ai, ensure_ascii=False)

    ai_analyze = await ai_service.get_ai_analyze(
        data=json_results,
        prompt=ai_service.PROMPTS["full_session"]
    )

    print(ai_analyze)
    await redis_service.delete_questions(session_id=session_id)

    return schemas.SessionCompleteResponse(
        session_id=session_id,
        results=results,
        overall_score=ai_analyze.get('score'),
        overall_feedback=ai_analyze.get('verdict')
    )
