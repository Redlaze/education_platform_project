from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.router import main_router
from app.core.database import init_models
from app.core.logging import setup_logger
from app.core.middlware import LoggerMiddleware

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup")
    logger.info("Application started successfully")
    # await init_models()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggerMiddleware)

app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
