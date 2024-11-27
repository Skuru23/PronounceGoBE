from sqlalchemy import select
from sqlmodel import Session

from models.lesson import Lesson
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.word import Word


def get_lesson_detail(db: Session, lesson_id: int):
    lesson = (
        db.exec(select(Lesson.__table__.columns).where(Lesson.id == lesson_id))
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
    lesson_senctences = (
        db.exec(
            select(LessonSentence.__table__.columns).where(
                LessonSentence.lesson_id == lesson_id
            )
        )
        .mappings()
        .all()
    )
    print(lesson_senctences)
    lesson = dict(lesson)
    lesson["word_list"] = lesson_words
    lesson["sentence_list"] = lesson_senctences

    return lesson
