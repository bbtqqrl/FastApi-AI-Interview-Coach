from typing import Annotated
from fastapi import FastAPI, Path
from contextlib import asynccontextmanager
import uvicorn
from core.models import Base, db_helper
from interview_sessions import router as router_v1
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
            }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)