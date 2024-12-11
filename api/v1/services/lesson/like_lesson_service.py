from sqlalchemy import select
from sqlmodel import Session
from models.lesson_like import LessonLike
from models.user import User


def like_lesson(db: Session, user: User, lesson_id):
    lesson_like = db.exec(
        select(LessonLike)
        .where(LessonLike.lesson_id == lesson_id)
        .where(LessonLike.user_id == user.id)
    ).first()

    if lesson_like:
        return
    else:
        db.add(LessonLike(lesson_id=lesson_id, user_id=user.id))
        db.commit()
        return
