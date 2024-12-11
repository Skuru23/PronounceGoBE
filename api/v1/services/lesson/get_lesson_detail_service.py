from sqlalchemy import case, select
from sqlmodel import Session

from models.group import Group
from models.lesson import Lesson
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.progress import Progress
from models.user import User
from models.word import Word


def get_lesson_detail(db: Session, user: User, lesson_id: int):
    lesson = (
        db.exec(
            select(
                Lesson.__table__.columns,
                User.name.label("creator_name"),
                Group.name.label("group_owner_name"),
            )
            .outerjoin(Progress, Progress.lesson_id == Lesson.id)
            .join(User, User.id == Lesson.user_owner_id)
            .where(Lesson.id == lesson_id)
        )
        .mappings()
        .first()
    )

    lesson_words = (
        db.exec(
            select(Word.__table__.columns)
            .join(LessonWord, LessonWord.word_id == Word.id)
            .where(LessonWord.lesson_id == lesson_id)
        )
        .mappings()
        .all()
    )
    lesson_sentences = (
        db.exec(
            select(LessonSentence.__table__.columns).where(
                LessonSentence.lesson_id == lesson_id
            )
        )
        .mappings()
        .all()
    )
    is_in_progress = db.exec(
        select(Progress)
        .where(Progress.lesson_id == lesson_id)
        .where(Progress.user_id == user.id)
    ).first()
    lesson = dict(lesson)
    lesson["words"] = lesson_words
    lesson["sentences"] = lesson_sentences
    lesson["is_in_progress"] = True if is_in_progress else False
    return lesson
