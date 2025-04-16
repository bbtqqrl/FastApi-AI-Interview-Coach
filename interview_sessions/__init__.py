from fastapi import APIRouter

from .views import router as session_router

router = APIRouter()

router.include_router(router=session_router, prefix="/session")