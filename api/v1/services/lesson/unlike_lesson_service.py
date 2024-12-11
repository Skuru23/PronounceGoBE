from sqlmodel import Session, select

from models.lesson_like import LessonLike
from models.user import User


def unlike_lesson(db: Session, user: User, lesson_id):
    lesson_like = db.exec(
        select(LessonLike)
        .where(LessonLike.lesson_id == lesson_id)
        .where(LessonLike.user_id == user.id)
    ).first()

    if not lesson_like:
        return
    else:
        db.delete(lesson_like)
        db.commit()
        return
