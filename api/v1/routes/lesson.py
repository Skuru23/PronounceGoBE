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
    LearnLessonResponse,
    ListLessonsResponse,
    UpdateLessonRequest,
)
from api.v1.services import lesson as lesson_services

router = APIRouter()


@router.post(
    "", status_code=HTTPStatus.NO_CONTENT, responses=authenticated_api_responses
)
def create_lesson(
    request: CreatePersonLessonRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson_services.create_lesson(db, user, request)


@router.get(
    "", response_model=ListLessonsResponse, responses=authenticated_api_responses
)
def listing_lessons(
    query: Annotated[GetLessonQuery, Depends(GetLessonQuery)],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lessons = lesson_services.get_lessons(db, query, user)

    return ListLessonsResponse(data=lessons)


@router.get(
    "/{lesson_id}",
    response_model=GetLessonDetailResponse,
    responses=authenticated_api_responses,
)
def get_lesson_detail(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = lesson_services.get_lesson_detail(db, user, lesson_id)
    return lesson


@router.post(
    "/{lesson_id}/learn",
    response_model=LearnLessonResponse,
    responses=authenticated_api_responses,
)
def learn_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress_id = lesson_services.learn_lesson(db, user, lesson_id)
    return LearnLessonResponse(progress=progress_id)


@router.put(
    "/{lesson_id}",
    status_code=HTTPStatus.NO_CONTENT,
    responses=authenticated_api_responses,
)
def update_lesson(
    lesson_id: int,
    request: UpdateLessonRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson_services.update_lesson(db, user, lesson_id, request)


@router.patch(
    "/{lesson_id}/like",
    status_code=HTTPStatus.NO_CONTENT,
    responses=authenticated_api_responses,
)
def like_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson_services.like_lesson(db, user, lesson_id)


@router.patch(
    "/{lesson_id}/unlike",
    status_code=HTTPStatus.NO_CONTENT,
    responses=authenticated_api_responses,
)
def unlike_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson_services.unlike_lesson(db, user, lesson_id)
