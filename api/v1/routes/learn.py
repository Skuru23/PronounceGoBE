from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses
from db.database import get_db
from models.user import User
from schemas.learn import (
    LearnWordRequest,
    LearnWordResponse,
    LearnSentenceRequest,
    LearnSentenceResponse,
)
from api.v1.services import learn as learn_services

router = APIRouter()


@router.post(
    "/words/{progress_word_id}",
    response_model=LearnWordResponse,
    responses=authenticated_api_responses,
)
def learn_word(
    progress_word_id: int,
    request: LearnWordRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return learn_services.learn_word(db, user, progress_word_id, request.speech_text)


@router.post(
    "/sentences/{progress_sentence_id}",
    response_model=LearnSentenceResponse,
    responses=authenticated_api_responses,
)
def learn_sentence(
    progress_sentence_id: int,
    request: LearnSentenceRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return learn_services.learn_sentence(
        db, user, progress_sentence_id, request.speech_text
    )
