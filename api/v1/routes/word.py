from http import HTTPStatus
from fastapi import APIRouter, Depends

from api.v1.dependencies.authentication import get_current_user
from models.user import User
from db.databse import get_db
from sqlmodel import Session
from core.config import settings
from core.response import authenticated_api_responses, public_api_responses
from api.v1.services import word as word_services
from schemas.word import WordDetailResponse

router = APIRouter()


@router.get(
    "/{word_id}",
    response_model=WordDetailResponse,
    responses=authenticated_api_responses,
)
def get_word_detail(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return word_services.get_word_detail(db, word_id)
