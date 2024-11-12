from fastapi import APIRouter

from .auth import router as auth_router
from .word import router as word_router
from .lesson import router as lesson_router
from .group import router as group_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"])
router.include_router(word_router, prefix="/words", tags=["words"])
router.include_router(lesson_router, prefix="/lessons", tags=["lessons"])
router.include_router(group_router, prefix="/groups", tags=["groups"])
