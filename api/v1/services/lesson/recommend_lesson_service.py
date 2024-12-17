from sqlalchemy import func, text
from sqlmodel import Session, select
from models.lesson import Lesson
from models.lesson_like import LessonLike
from models.progress import Progress
from models.user import User


def recommend_lesson(db: Session):
    new_lessons = (
        db.exec(
            select(
                Lesson.id,
                Lesson.name,
                Lesson.description,
                Lesson.image_path,
                Lesson.is_public,
                Lesson.user_owner_id,
                Lesson.group_owner_id,
            )
            .where(Lesson.is_public == True)
            .order_by(Lesson.created_at.desc())
            .limit(5)
        )
        .mappings()
        .all()
    )

    hot_lesson = (
        db.exec(
            select(
                Lesson.id,
                Lesson.name,
                Lesson.description,
                Lesson.image_path,
                Lesson.is_public,
                Lesson.user_owner_id,
                Lesson.group_owner_id,
                (
                    func.count(LessonLike.id.distinct())
                    + func.count(Progress.id.distinct())
                ).label("total_score"),
            )
            .join(LessonLike, LessonLike.lesson_id == Lesson.id, isouter=True)
            .join(Progress, Progress.lesson_id == Lesson.id, isouter=True)
            .where(Lesson.is_public == True)
            .group_by(Lesson.id)
            .order_by(text("total_score desc"))
            .limit(5)
        )
        .mappings()
        .all()
    )

    return new_lessons, hot_lesson
