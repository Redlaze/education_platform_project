from fastapi import APIRouter

from app.api import admin, auth, course, student


main_router = APIRouter()

main_router.include_router(admin.router)
main_router.include_router(auth.router)
main_router.include_router(course.router)
main_router.include_router(student.router)
