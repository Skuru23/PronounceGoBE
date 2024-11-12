from sqlmodel import Session

from models.lesson import Lesson
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.user import User
from schemas.lesson import CreatePersonLessonRequest


def create_lesson(db: Session, user: User, request: CreatePersonLessonRequest):
    try:
        lesson = Lesson(
            name=request.name,
            description=request.description,
            user_owner_id=user.id,
            is_public=request.is_public,
            created_by=user.id,
        )
        db.add(lesson)
        db.flush()

        word_list = [
            LessonWord(lesson_id=lesson.id, word_id=id) for id in request.word_ids
        ]
        db.add_all(word_list)
        db.flush

        sentence_list = [
            LessonSentence(lesson_id=lesson.id, sentence=sentence)
            for sentence in request.sentence_list
        ]
        db.add_all(sentence_list)
        db.flush

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
