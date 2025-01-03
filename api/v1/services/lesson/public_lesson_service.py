from sqlmodel import Session, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.lesson import Lesson
from models.user import User


def public_lesson(db: Session, user: User, lesson_id: int):
    lesson = db.exec(select(Lesson).where(Lesson.id == lesson_id)).first()
    if not lesson:
        raise BadRequestException(
            ErrorCode.ERR_LESSON_NOT_EDITABLE, ErrorMessage.ERR_LESSON_NOT_EDITABLE
        )

    if lesson.user_owner_id != user.id:
        if lesson.group_owner_id is not None:
            if lesson.group_owner_id != user.group_id:
                raise BadRequestException(
                    ErrorCode.ERR_LESSON_NOT_EDITABLE,
                    ErrorMessage.ERR_LESSON_NOT_EDITABLE,
                )
        else:
            raise BadRequestException(
                ErrorCode.ERR_LESSON_NOT_EDITABLE, ErrorMessage.ERR_LESSON_NOT_EDITABLE
            )

    lesson.is_public = True
    db.add(lesson)
    db.commit()
