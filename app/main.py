from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.router import main_router
from app.core.database import init_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)