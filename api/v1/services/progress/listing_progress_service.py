from sqlalchemy import func
from sqlmodel import Session, select

from models.lesson import Lesson
from models.progress import Progress
from models.progress_sentence import ProgressSentence
from models.progress_word import ItemStatus, ProgressWord
from models.user import User


def listing_progress(db: Session, user: User):
    subquery = (
        select(
            Progress.id,
            func.count(ProgressWord.id.distinct()).label("remain_word"),
            func.count(ProgressSentence.id.distinct()).label("remain_sentence"),
        )
        .outerjoin(ProgressWord, ProgressWord.progress_id == Progress.id)
        .outerjoin(ProgressSentence, ProgressSentence.progress_id == Progress.id)
        .where(ProgressWord.status.isnot(ItemStatus.DONE))
        .group_by(Progress.id)
        .subquery()
    )

    progress = db.exec(
        select(
            Progress.id,
            Progress.lesson_id,
            Lesson.name,
            func.count(ProgressWord.id.distinct()).label("total_word"),
            func.count(ProgressSentence.id.distinct()).label("total_sentence"),
            func.max(subquery.c.remain_word),
            func.max(subquery.c.remain_sentence),
        )
        .join(Lesson, Lesson.id == Progress.lesson_id)
        .outerjoin(ProgressWord, ProgressWord.progress_id == Progress.id)
        .outerjoin(ProgressSentence, ProgressSentence.progress_id == Progress.id)
        .join(subquery, subquery.c.id == Progress.id)
        .where(Progress.user_id == user.id)
        .group_by(Progress.id)
        .order_by(Progress.id.desc())
    ).mappings().all()
    
    for item in progress:
        item['finish_percent'] = item.
