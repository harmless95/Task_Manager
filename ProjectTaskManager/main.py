import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status

from core.config import setting
from core.model import db_helper
from api.routers import all_routers

logging.basicConfig(
    level=logging.INFO,
    format=setting.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app_main = FastAPI(lifespan=lifespan)
app_main.include_router(router=all_routers)


@app_main.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_hello():
    return {
        "message": "Hello, the task manager container is running!",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=setting.run.host,
        port=setting.run.port,
    )
