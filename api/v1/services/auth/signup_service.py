from schemas.auth import SignupRequest
from models.user import User, RoleCode
from sqlmodel import Session, select
from core.exception import BadRequestException, ErrorCode, ErrorMessage
from utils import get_password_hash


def signup(db: Session, request: SignupRequest):
    try:
        user = db.exec(select(User).where(User.email == request.email)).one_or_none()
        if user:
            raise BadRequestException(
                ErrorCode.ERR_USER_EXISTED, ErrorMessage.ERR_USER_EXISTED
            )

        user = User(
            role_code=RoleCode.USER,
            email=request.email,
            password=get_password_hash(request.password),
            name=request.name,
            phone=request.phone,
            address=request.address,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback
        raise e
