from datetime import datetime
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select
from core.config import settings

from core.exception import ErrorCode, UnauthorizedException
from db.databse import get_db
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/", auto_error=False)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if token:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email = payload.get("sub")
            if (
                email is None
                or not isinstance(email, str)
                or datetime.now().timestamp() > payload.get("exp")
            ):
                raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)
        except Exception:
            raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)
        user = db.exec(select(User).where(User.email == email)).one_or_none()
        if not user:
            raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)
        return user
    else:
        raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)


def get_user_if_logged_in(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if token:
        return get_current_user(db, token)

    return None
