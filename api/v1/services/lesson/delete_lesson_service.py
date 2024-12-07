from sqlalchemy import delete
from sqlmodel import Session, select
from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group_member import GroupMember
from models.lesson import Lesson
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.progress import Progress
from models.progress_sentence import ProgressSentence
from models.progress_word import ProgressWord
from models.user import User


def delete_lesson(db: Session, user: User, lesson_id: int):
    lesson = db.exec(select(Lesson).where(Lesson.id == lesson_id)).first()
    if lesson.user_owner_id != user.id:
        if lesson.group_owner_id:
            edit_permission = db.exec(
                select(GroupMember)
                .where(GroupMember.group_id == lesson.group_owner_id)
                .where(GroupMember.user_id == user.id)
                .where(GroupMember.is_manager)
            ).first()

            if not edit_permission:
                raise BadRequestException(
                    ErrorCode.ERR_ACCESS_DENIED, ErrorMessage.ERR_ACCESS_DENIED
                )
        else:
            raise BadRequestException(
                ErrorCode.ERR_ACCESS_DENIED, ErrorMessage.ERR_ACCESS_DENIED
            )

    if lesson.is_public or (lesson.group_owner_id is not None):
        not_deletable = db.exec(Progress).where(Progress.lesson_id == lesson_id)
        if not_deletable:
            raise BadRequestException(
                ErrorCode.ERR_LESSON_NOT_EDITABLE, ErrorMessage.ERR_LESSON_NOT_EDITABLE
            )
    try:
        db.exec(
            delete(ProgressWord)
            .where(ProgressWord.progress_id == Progress.id)
            .where(Progress.lesson_id == lesson_id)
        )
        db.exec(
            delete(ProgressSentence)
            .where(ProgressSentence.progress_id == Progress.id)
            .where(Progress.lesson_id == lesson_id)
        )
        db.exec(delete(Progress).where(Progress.lesson_id == lesson_id))
        db.exec(delete(LessonWord).where(LessonWord.lesson_id == lesson.id))
        db.exec(delete(LessonSentence).where(LessonSentence.lesson_id == lesson.id))
        db.exec(delete(Lesson).where(lesson_id == lesson_id))

    except Exception as e:
        db.rollback()
        raise e
