from sqlalchemy import func
from sqlmodel import Session, case, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group import Group
from models.lesson import Lesson
from models.progress import Progress
from models.progress_sentence import ProgressSentence
from models.progress_word import ItemStatus, ProgressWord
from models.user import User


def get_progress_detail(db: Session, progress_id: int):
    progress = db.exec(select(Progress).where(Progress.id == progress_id)).first()

    if not progress:
        raise BadRequestException(
            ErrorCode.ERR_PROGRESS_NOT_FOUND, ErrorMessage.ERR_PROGRESS_NOT_FOUND
        )

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

    progress_query = (
        select(
            Progress.id,
            Progress.lesson_id,
            Lesson.name.label("lesson_name"),
            User.name.label("creator_name"),
            Group.name.label("group_owner_name"),
            func.count(ProgressWord.id.distinct()).label("total_word"),
            func.count(ProgressSentence.id.distinct()).label("total_sentence"),
            subquery.c.remain_word,
            subquery.c.remain_sentence,
        )
        .join(Lesson, Progress.lesson_id == Lesson.id)
        .join(User, User.id == Lesson.user_owner_id)
        .outerjoin(Group, Group.id == Lesson.group_owner_id)
        .outerjoin(ProgressWord, ProgressWord.progress_id == Progress.id)
        .outerjoin(ProgressSentence, ProgressSentence.progress_id == Progress.id)
        .outerjoin(subquery, subquery.c.id == Progress.id)
        .where(Progress.id == progress_id)
        .group_by(Progress.id, Lesson.name, User.name, Group.name)
    )

    progress = db.exec(progress_query).mappings().first()
    progress = dict(progress)

    progress["finish_percent"] = int(
        (
            1
            - (
                (progress["remain_word"] + progress["remain_sentence"])
                / (progress["total_word"] + progress["total_sentence"])
            )
        )
        * 100
    )

    return progress
