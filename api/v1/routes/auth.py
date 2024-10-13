from http import HTTPStatus
from fastapi import APIRouter, Depends

from schemas.auth import LoginResponse, LoginRequest, SignupRequest, TokenResponse
from db.databse import get_db
from sqlmodel import Session
from core.config import settings
from core.response import authenticated_api_responses, public_api_responses
from api.v1.services import auth as auth_services

router = APIRouter()


@router.post("/login", response_model=TokenResponse, responses=public_api_responses)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_services.login(request, db)


@router.post(
    "/signup", status_code=HTTPStatus.NO_CONTENT, responses=public_api_responses
)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return auth_services.signup(db, request)


@router.get(
    "/refresh-token", response_model=TokenResponse, responses=public_api_responses
)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    return auth_services.refresh_token(db, refresh_token)
