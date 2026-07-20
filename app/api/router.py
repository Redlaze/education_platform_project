from fastapi import APIRouter

from app.api import user
from app.api import auth

main_router = APIRouter()

main_router.include_router(user.router)
main_router.include_router(auth.router)
