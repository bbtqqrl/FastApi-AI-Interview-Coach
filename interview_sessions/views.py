from fastapi import APIRouter
router = APIRouter(tags=["sessions"])

@router.get("/")
async def get_prooducts():
    return {"session_list": ["Hello World"]}

