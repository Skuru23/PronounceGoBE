from sqlalchemy import func
from sqlmodel import Session, select
from models.group import Group
from models.group_member import GroupMember
from models.lesson import Lesson
from models.progress import Progress
from models.progress_sentence import ProgressSentence
from models.progress_word import ItemStatus, ProgressWord
from models.user import User


def get_user_detail(db: Session, user: User):
    user_detail = db.exec(select(User).where(User.id == user.id)).first()
    user_detail = dict(user_detail)

    subquery = (
        select(
            Progress.id,
            func.count(ProgressWord.id.distinct()).label("remain_word"),
            func.count(ProgressSentence.id.distinct()).label("remain_sentence"),
        )
        .outerjoin(ProgressWord, ProgressWord.progress_id == Progress.id)
        .outerjoin(ProgressSentence, ProgressSentence.progress_id == Progress.id)
        .where(ProgressWord.status != ItemStatus.DONE)
        .group_by(Progress.id)
        .subquery()
    )

    progress = (
        db.exec(
            select(
                Progress.id,
                func.count(ProgressWord.id.distinct()).label("total_word"),
                func.count(ProgressSentence.id.distinct()).label("total_sentence"),
                subquery.c.remain_word.label("remain_word"),
                subquery.c.remain_sentence.label("remain_sentence"),
            )
            .outerjoin(ProgressWord, ProgressWord.progress_id == Progress.id)
            .outerjoin(ProgressSentence, ProgressSentence.progress_id == Progress.id)
            .outerjoin(subquery, subquery.c.id == Progress.id)
            .where(Progress.user_id == user.id)
            .group_by(Progress.id)
        )
        .mappings()
        .all()
    )

    total_progress = len(progress)
    completed_progress = sum(
        1 for p in progress if p["remain_word"] == 0 and p["remain_sentence"] == 0
    )
    user_detail["total_progress"] = total_progress
    user_detail["done_progress"] = completed_progress
    user_detail["remain_progress"] = total_progress - completed_progress

    total_lesson = db.exec(
        select(func.count(Lesson.id)).where(Lesson.user_owner_id == user.id)
    ).first()
    user_detail["total_lesson"] = total_lesson

    joined_group = db.exec(
        select(func.count(GroupMember.id)).where(GroupMember.user_id == user.id)
    ).first()
    user_detail["joined_group"] = joined_group

    return user_detail
