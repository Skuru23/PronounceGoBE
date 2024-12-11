from fastapi import APIRouter

from .auth import router as auth_router
from .word import router as word_router
from .lesson import router as lesson_router
from .group import router as group_router
from .progress import router as progress_router
from .learn import router as learn_router
from .image import router as image_router
from .user import router as user_router
from .member import router as member_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"])
router.include_router(word_router, prefix="/words", tags=["words"])
router.include_router(lesson_router, prefix="/lessons", tags=["lessons"])
router.include_router(group_router, prefix="/groups", tags=["groups"])
router.include_router(progress_router, prefix="/progresses", tags=["progress"])
router.include_router(learn_router, prefix="/learn", tags=["learn"])
router.include_router(image_router, prefix="/images", tags=["images"])
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(member_router, prefix="/members", tags=["members"])
