from typing import Annotated
from fastapi import FastAPI, Path
from contextlib import asynccontextmanager
import uvicorn
from core.models import Base
from core.db_helper import db_helper
from core.config import settings
from api.users.views import router as users_router
from api.topics.views import router as topics_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=users_router, prefix=settings.api_v1_prefix)
app.include_router(router=topics_router, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)