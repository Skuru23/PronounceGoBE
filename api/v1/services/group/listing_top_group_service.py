from sqlalchemy import func, text
from sqlmodel import Session, select

from models.group import Group
from models.group_member import GroupMember
from models.lesson import Lesson


def listing_top_group(db: Session):
    groups = (
        db.exec(
            select(
                Group.id,
                Group.name,
                Group.description,
                Group.image_path,
                Group.owner_id,
                (
                    func.count(GroupMember.id.distinct())
                    + func.count(Lesson.id.distinct())
                ).label("point"),
            )
            .outerjoin(GroupMember, GroupMember.group_id == Group.id)
            .outerjoin(Lesson, Lesson.group_owner_id == Group.id)
            .group_by(Group.id)
            .order_by(text("point desc"))
            .limit(5)
        )
        .mappings()
        .all()
    )

    return groups
