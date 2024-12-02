from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses, public_api_responses
from db.database import get_db
from models.user import User
from schemas.lesson import (
    CreatePersonLessonRequest,
    GetLessonDetailResponse,
    GetLessonQuery,
    ListLessonsResponse,
)
from api.v1.services import progress as progress_services
from schemas.progress import ListingProgressResponse, ProgressDetailResponse

router = APIRouter()


@router.get("", response_model=ListingProgressResponse, responses=public_api_responses)
def listing_progress(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    progresses = progress_services.listing_progress(db, user)

    return ListingProgressResponse(data=progresses)


@router.get(
    "/{progress_id}",
    response_model=ProgressDetailResponse,
    responses=public_api_responses,
)
def get_progress_detail(
    progress_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = progress_services.get_progress_detail(db, progress_id)
    return progress


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
