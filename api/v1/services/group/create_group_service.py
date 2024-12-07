from sqlmodel import Session, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group import Group
from models.group_member import GroupMember
from models.user import User
from schemas.group import CreateGroupRequest


def create_group(db: Session, user: User, request: CreateGroupRequest):
    try:
        existed_group = db.exec(select(Group).where(Group.name == request.name)).first()

        if existed_group:
            raise BadRequestException(
                ErrorCode.ERR_GROUP_EXISTED, ErrorMessage.ERR_GROUP_EXISTED
            )

        group = Group(
            name=request.name,
            description=request.description,
            owner_id=user.id,
            image_path=request.image_path,
        )
        db.add(group)
        db.flush()

        first_member = GroupMember(group_id=group.id, user_id=user.id, is_manager=True)
        db.add(first_member)
        db.flush()
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
