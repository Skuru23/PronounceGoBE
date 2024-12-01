from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses, public_api_responses
from db.databse import get_db
from models.user import User
from schemas.lesson import (
    CreatePersonLessonRequest,
    GetLessonDetailResponse,
    GetLessonQuery,
    ListLessonsResponse,
)
from api.v1.services import lesson as lesson_services
from schemas.progress import ListingProgressResponse

router = APIRouter()


@router.get("", response_model=ListingProgressResponse, responses=public_api_responses)
def listing_progress(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    lessons = lesson_services.get_lessons(db, query)

    return ListLessonsResponse(data=lessons)


# @router.get(
#     "/{lesson_id}",
#     response_model=GetLessonDetailResponse,
#     responses=public_api_responses,
# )
# def listing_lessons(
#     lesson_id: int,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user),
# ):
#     lesson = lesson_services.get_lesson_detail(db, lesson_id)
#     return lesson


# @router.post(
#     "/{lesson_id}/learn",
#     status_code=HTTPStatus.NO_CONTENT,
#     responses=authenticated_api_responses,
# )
# def learn_lesson(
#     lesson_id: int,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user),
# ):
#     lesson_services.learn_lesson(db, user, lesson_id)
