from sqlmodel import Session, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group import Group
from models.group_member import GroupMember
from models.user import User


def join_group(db: Session, user: User, group_id: int):
    group = db.exec(select(Group).where(Group.id == group_id)).first()

    if not group:
        raise BadRequestException(
            error_code=ErrorCode.ERR_GROUP_NOT_FOUND,
            message=ErrorMessage.ERR_GROUP_NOT_FOUND,
        )

    is_member = db.exec(
        select(GroupMember).where(
            GroupMember.group_id == group_id, GroupMember.user_id == user.id
        )
    ).first()

    if is_member:
        if is_member.approved_at:
            raise BadRequestException(
                error_code=ErrorCode.ERR_USER_ALREADY_JOINED_GROUP,
                message=ErrorMessage.ERR_USER_ALREADY_JOINED_GROUP,
            )
        else:
            raise BadRequestException(
                error_code=ErrorCode.ERR_USER_ALREADY_JOINED_GROUP,
                message="Your request is pending",
            )

    db.add(GroupMember(group_id=group_id, user_id=user.id))
    db.commit()
