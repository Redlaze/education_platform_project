from fastapi import APIRouter

from app.api import admin
from app.api import auth
from app.api import course

main_router = APIRouter()

main_router.include_router(admin.router)
main_router.include_router(auth.router)
main_router.include_router(course.router)
