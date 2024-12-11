from sqlalchemy import and_, case, func, literal
from sqlmodel import Session, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group import Group
from models.group_member import GroupMember
from models.lesson import Lesson
from models.user import User


def get_group_detail(db: Session, user: User, group_id: int):
    subquery = (
        select(
            Group.id,
            func.count(GroupMember.id.distinct()).label("total_member"),
            func.count(Lesson.id.distinct()).label("total_lesson"),
            literal(0).label("total_like"),
        )
        .outerjoin(GroupMember, GroupMember.group_id == Group.id)
        .outerjoin(Lesson, Lesson.group_owner_id == Group.id)
        .group_by(Group.id)
        .subquery()
    )

    group = (
        db.exec(
            select(
                Group.id,
                Group.name,
                Group.description,
                Group.owner_id,
                Group.image_path,
                User.name.label("creator"),
                subquery.c.total_member,
                subquery.c.total_lesson,
                subquery.c.total_like,
                case((GroupMember.user_id == user.id, True), else_=False).label(
                    "is_member"
                ),
                case((GroupMember.is_manager.is_(True), True), else_=False).label(
                    "is_owner"
                ),
            )
            .outerjoin(User, User.id == Group.owner_id)
            .outerjoin(subquery, subquery.c.id == Group.id)
            .outerjoin(
                GroupMember,
                and_(
                    GroupMember.group_id == Group.id,
                    GroupMember.approved_at.isnot(None),
                    GroupMember.user_id == user.id,
                ),
            )
            .where(Group.id == group_id)
        )
        .mappings()
        .first()
    )

    if not group:
        raise BadRequestException(
            ErrorCode.ERR_GROUP_EXISTED, ErrorMessage.ERR_GROUP_EXISTED
        )

    return group
