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
    GetLessonQuery,
    ListLessonsResponse,
)
from api.v1.services import lesson as lesson_services

router = APIRouter()


@router.post(
    "", status_code=HTTPStatus.NO_CONTENT, responses=authenticated_api_responses
)
def create_person_lesson(
    request: CreatePersonLessonRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson_services.create_lesson(db, user, request)


@router.get("", response_model=ListLessonsResponse, responses=public_api_responses)
def listing_lessons(
    query: Annotated[GetLessonQuery, Depends(GetLessonQuery)],
    db: Session = Depends(get_db),
):
    lessons = lesson_services.get_lessons(db, query)

    return ListLessonsResponse(data=lessons)