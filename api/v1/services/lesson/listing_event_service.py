from typing import List, Dict, Any
from sqlalchemy import and_, case, func
from sqlmodel import Session, select
from models import Lesson
from models.group_member import GroupMember
from models.lesson_like import LessonLike
from models.progress import Progress
from models.user import User
from schemas.lesson import (
    GetLessonQuery,
)  # Assuming you have a Lesson model defined in models.py


def get_lessons(db: Session, query_params: GetLessonQuery, user: User):
    learner_subquery = (
        select(Lesson.id, func.count(Progress.id).label("total_learners"))
        .outerjoin(Progress, Progress.lesson_id == Lesson.id)
        .group_by(Lesson.id)
    ).subquery()

    like_subquery = (
        select(Lesson.id, func.count(LessonLike.id).label("total_likes"))
        .outerjoin(LessonLike, LessonLike.lesson_id == Lesson.id)
        .group_by(Lesson.id)
    ).subquery()

    base_query = (
        select(
            Lesson.id,
            Lesson.name,
            Lesson.description,
            Lesson.user_owner_id,
            Lesson.group_owner_id,
            Lesson.is_public,
            Lesson.image_path,
            User.name.label("creator"),
            case((LessonLike.user_id == user.id, True), else_=False).label("is_liked"),
            learner_subquery.c.total_learners.label("total_learners"),
            like_subquery.c.total_likes.label("total_likes"),
        )
        .outerjoin(learner_subquery, learner_subquery.c.id == Lesson.id)
        .outerjoin(like_subquery, like_subquery.c.id == Lesson.id)
        .outerjoin(
            LessonLike,
            and_(LessonLike.lesson_id == Lesson.id, LessonLike.user_id == user.id),
        )
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
        is_member = db.exec(
            select(GroupMember.id).where(
                and_(
                    GroupMember.group_id == int(query_params.group_owner_id),
                    GroupMember.user_id == user.id,
                )
            )
        ).first()
        if not is_member and query_params.is_public == False:
            return []

    if query_params.keyword:
        base_query = base_query.where(Lesson.name.contains(query_params.keyword))

    lessons = db.exec(base_query).mappings().all()

    return lessons
