from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends

from api.v1.dependencies.authentication import get_current_user, get_user_if_logged_in
from models.user import User
from schemas.auth import (
    GetMeResponse,
    LoginResponse,
    LoginRequest,
    SignupRequest,
    TokenResponse,
)
from db.database import get_db
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


@router.get("/me", response_model=GetMeResponse, responses=authenticated_api_responses)
async def me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return GetMeResponse(
        id=current_user.id,
        role_code=current_user.role_code,
        email=current_user.email,
        name=current_user.name,
        phone=current_user.phone,
        address=current_user.address,
        image_path=current_user.image_path,
    )
