from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter(tags=["sessions"])

@router.get("/")
async def get_prooducts(session: AsyncSession = Depends(db_helper.session_dependency)):
    try:
        result = await session.execute(text("SELECT 1"))
        return {"success": result.scalar() == 1}
    except Exception as e:
        return {"success": False, "error": str(e)}