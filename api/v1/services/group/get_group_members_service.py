from sqlmodel import Session, select

from models.group_member import GroupMember
from models.user import User


def get_group_members(db: Session, user: User, group_id: int):
    members = (
        db.exec(
            select(
                GroupMember.id,
                GroupMember.user_id,
                GroupMember.approved_at,
                User.name,
                GroupMember.is_manager,
            )
            .join(User, User.id == GroupMember.user_id)
            .where(GroupMember.group_id == group_id)
            .order_by(GroupMember.created_at.desc())
        )
        .mappings()
        .all()
    )

    return members
