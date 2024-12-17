from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlmodel import Session
from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses
from db.database import get_db
from models.user import User
from schemas.user import UpdateUserRequest, UserResponse
from api.v1.services import user as user_services

router = APIRouter()


@router.put(
    "", status_code=HTTPStatus.NO_CONTENT, responses=authenticated_api_responses
)
def update_user(
    request: UpdateUserRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    user_services.update_information(db, user, request)


@router.get("", response_model=UserResponse, responses=authenticated_api_responses)
def get_user(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return user_services.get_user_detail(db, user)
