from datetime import datetime
from sqlmodel import Session, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group_member import GroupMember
from models.user import User


def approve_member(db: Session, user: User, member_id: int):
    group_member = db.exec(
        select(GroupMember).where(GroupMember.id == member_id)
    ).first()

    if not group_member:
        raise BadRequestException(
            error_code=ErrorCode.ERR_GROUP_MEMBER_NOT_FOUND,
            message=ErrorMessage.ERR_GROUP_MEMBER_NOT_FOUND,
        )

    is_manager = db.exec(
        select(GroupMember)
        .where(GroupMember.user_id == user.id)
        .where(GroupMember.group_id == group_member.group_id)
        .where(GroupMember.is_manager.is_(True))
    ).first()

    if not is_manager:
        raise BadRequestException(
            error_code=ErrorCode.ERR_USER_NOT_MANAGER,
            message=ErrorMessage.ERR_USER_NOT_MANAGER,
        )

    group_member.approved_at = datetime.now()
    db.add(group_member)
    db.commit()
