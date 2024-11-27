from sqlalchemy import func, literal
from sqlmodel import Session, or_, select

from models.group import Group
from models.group_member import GroupMember
from models.lesson import Lesson
from models.user import User
from schemas.group import GetGroupsQueryParams


def listing_group(db: Session, query_params: GetGroupsQueryParams):
    conditions = _build_conditions(query_params)

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
            User.name.label("creator"),
            subquery.c.total_member,
            subquery.c.total_lesson,
            subquery.c.total_like,
        )
        .join(User, User.id == Group.owner_id)
        .join(subquery, subquery.c.id == Group.id)
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


def _build_conditions(query_params: GetGroupsQueryParams):
    conditions = []
    if query_params.name:
        conditions.append(
            or_(
                func.lower(Group.name).contains(query_params.name),
                func.lower(User.name).contains(query_params.name),
            )
        )

    return conditions
