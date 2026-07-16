from fastapi import APIRouter

from app.api import user

main_router = APIRouter()

main_router.include_router(user.router)