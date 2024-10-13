from datetime import datetime, timedelta
import jwt

from sqlmodel import select, Session
from core.config import settings
from core.exception import UnauthorizedException, ErrorCode
from models.user import User
from schemas.auth import TokenResponse


def refresh_token(db: Session, refresh_token: str):
    payload = jwt.decode(
        refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    if payload["exp"] < datetime.now().timestamp():
        raise UnauthorizedException(ErrorCode.ERR_TOKEN_EXPIRED)
    if not payload["sub"]:
        raise UnauthorizedException(ErrorCode.ERR_UNAUTHORIZED)
    user = db.exec(select(User).where(User.email == payload["sub"])).first()

    if not user:
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
