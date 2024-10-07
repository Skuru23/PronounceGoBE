from http import HTTPStatus
from fastapi import APIRouter, Depends

from schemas.auth import LoginResponse, LoginRequest, SignupRequest
from db.databse import get_db
from sqlmodel import Session
from core.config import settings
from api.v1.services import auth as auth_services

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    print(settings.SQLALCHEMY_DATABASE_URL)
    return LoginResponse(id=2)


@router.post("/signup", status_code=HTTPStatus.NO_CONTENT)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    return auth_services.signup(db, request)
