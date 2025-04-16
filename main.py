from typing import Annotated
from fastapi import FastAPI, Path
from contextlib import asynccontextmanager
import uvicorn
from interview_sessions import router as router_v1
from core.config import settings


app = FastAPI()

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
            }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)