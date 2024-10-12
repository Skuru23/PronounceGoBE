from datetime import datetime, timedelta
from sqlmodel import Session, select
import jwt
from models.user import User
from schemas.auth import LoginRequest, TokenResponse
from core.config import settings
from core.exception import UnauthorizedException, ErrorCode
from utils import verify_password


def login(request: LoginRequest, db: Session):
    user = db.exec(select(User).where(User.email == request.email)).first()

    if (not user) or (not verify_password(request.password, user.password)):
        raise UnauthorizedException(ErrorCode.ERR_UNAUTHORIZED)
    access_token_expires = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token_data = {
        "sub": user.email,
        "role": user.role_code,
        "exp": access_token_expires,
    }
    access_token = jwt.encode(
        access_token_data, settings.SECRET_KEY, settings.ALGORITHM
    )

    refresh_token_expires = datetime.now() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    refresh_token_data = {
        "sub": user.email,
        "role": user.role_code,
        "exp": refresh_token_expires,
    }
    refresh_token = jwt.encode(
        refresh_token_data, settings.SECRET_KEY, settings.ALGORITHM
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expire_at=access_token_expires,
        refresh_token=refresh_token,
        refresh_expire_at=refresh_token_expires,
    )
