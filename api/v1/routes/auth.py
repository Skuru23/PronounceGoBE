from fastapi import APIRouter, Depends

from schemas.auth import LoginResponse, LoginRequest, SignupRequest
from db.databse import get_db
from sqlmodel import Session
from core.config import settings

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    print(settings.SQLALCHEMY_DATABASE_URL)
    return LoginResponse(id=2)

@router.post("/signup", response_model=LoginResponse)
def signup(request: SignupRequest):
    return LoginResponse(id=1)