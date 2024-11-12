from http import HTTPStatus
from fastapi import APIRouter, Depends

from api.v1.dependencies.authentication import get_current_user
from models.user import User
from db.databse import get_db
from sqlmodel import Session
from core.config import settings
from core.response import authenticated_api_responses, public_api_responses
from api.v1.services import word as word_services
from schemas.word import (
    CheckPronounceRequest,
    CheckPronounceResponse,
    WordDetailResponse,
)

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


@router.post(
    "/check",
    response_model=CheckPronounceResponse,
    responses=authenticated_api_responses,
)
def check_pronounce(
    request: CheckPronounceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    score, ipa, errors = word_services.check_pronounce(db, request)
    return CheckPronounceResponse(
        text=request.expect_text, ipa=ipa, error=errors, point=score
    )
