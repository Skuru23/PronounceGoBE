from typing import List, Dict, Any
from sqlalchemy import func
from sqlmodel import Session, select
from models import Lesson
from models.lesson_like import LessonLike
from models.user import User
from schemas.lesson import (
    GetLessonQuery,
)  # Assuming you have a Lesson model defined in models.py


def get_lessons(db: Session, query_params: GetLessonQuery):
    base_query = (
        select(
            Lesson.id,
            Lesson.name,
            Lesson.description,
            Lesson.user_owner_id,
            Lesson.group_owner_id,
            Lesson.is_public,
            User.name.label("creator"),
            func.count(LessonLike.id).label("total_like"),
        )
        .outerjoin(LessonLike, Lesson.id == LessonLike.lesson_id)
        .join(User, Lesson.user_owner_id == User.id)
        .group_by(Lesson.id)
        .order_by(Lesson.created_at.desc())
    )

    if not query_params.is_public:
        base_query = base_query.where(Lesson.is_public.is_(False))
    else:
        base_query = base_query.where(Lesson.is_public.is_(True))

    if query_params.user_owner_id and (len(query_params.user_owner_id) > 0):
        base_query = base_query.where(
            Lesson.user_owner_id == int(query_params.user_owner_id)
        )

    if query_params.group_owner_id and (len(query_params.group_owner_id) > 0):
        base_query = base_query.where(
            Lesson.group_owner_id == int(query_params.group_owner_id)
        )

    if query_params.keyword:
        base_query = base_query.where(Lesson.name.contains(query_params.keyword))

    lessons = db.exec(base_query).mappings().all()
    return lessons
