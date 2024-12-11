from http import HTTPStatus
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from sqlmodel import Session

from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses
from db.database import get_db
from models.user import User
from api.v1.services import member as member_services

router = APIRouter()


# Mock database
@router.post(
    "/{member_id}/approve",
    status_code=HTTPStatus.NO_CONTENT,
    responses=authenticated_api_responses,
)
def approve_member(
    member_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    member_services.approve_member(db, user, member_id)
