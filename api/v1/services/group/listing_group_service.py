from sqlalchemy import and_, case, func, literal
from sqlmodel import Session, or_, select

from models.group import Group
from models.group_member import GroupMember
from models.lesson import Lesson
from models.user import User
from schemas.group import GetGroupsQueryParams


def listing_group(db: Session, user: User, query_params: GetGroupsQueryParams):
    conditions = _build_conditions(db, query_params, user)

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

    query = (
        select(
            Group.id,
            Group.name,
            Group.description,
            Group.owner_id,
            Group.image_path,
            User.name.label("creator"),
            case((GroupMember.user_id == user.id, True), else_=False).label(
                "is_member"
            ),
            subquery.c.total_member,
            subquery.c.total_lesson,
            subquery.c.total_like,
        )
        .join(User, User.id == Group.owner_id)
        .join(subquery, subquery.c.id == Group.id)
        .outerjoin(
            GroupMember,
            and_(
                GroupMember.group_id == Group.id,
                GroupMember.approved_at.isnot(None),
                GroupMember.user_id == user.id,
            ),
        )
        .where(*conditions)
        .order_by(Group.id.desc())
        # .limit(query_params.per_page)
        # .offset((query_params.page - 1) * query_params.per_page)
    )

    groups = db.exec(query).mappings().all()
    total = _count_group(db, conditions)
    return groups, total


def _count_group(db: Session, conditions: list):
    query = (
        select(func.count(Group.id))
        .join(User, User.id == Group.owner_id)
        .where(*conditions)
    )

    total = db.exec(query).first()
    return total


def _build_conditions(db: Session, query_params: GetGroupsQueryParams, user: User):
    conditions = []
    if query_params.name:
        conditions.append(
            or_(
                func.lower(Group.name).contains(query_params.name),
                func.lower(User.name).contains(query_params.name),
            )
        )

    if query_params.is_member:
        if bool(query_params.is_member):
            group_ids = db.exec(
                select(GroupMember.group_id).where(GroupMember.user_id == user.id)
            ).all()
            conditions.append(Group.id.in_(group_ids))

    return conditions
