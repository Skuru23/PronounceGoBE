from sqlalchemy import delete
from sqlmodel import Session, select
from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.group_member import GroupMember
from models.lesson import Lesson
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.progress import Progress
from models.user import User
from schemas.lesson import UpdateLessonRequest


def update_lesson(
    db: Session, user: User, lesson_id: int, request: UpdateLessonRequest
):
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

    not_editable = db.exec(
        select(Progress).where(Progress.lesson_id == lesson_id)
    ).first()

    if not_editable:
        raise BadRequestException(
            ErrorCode.ERR_LESSON_NOT_EDITABLE, ErrorMessage.ERR_LESSON_NOT_EDITABLE
        )
    try:
        db.exec(delete(LessonWord).where(LessonWord.lesson_id == lesson_id))
        word_list = [
            LessonWord(lesson_id=lesson.id, word_id=id) for id in request.word_ids
        ]
        db.add_all(word_list)

        db.exec(delete(LessonSentence).where(LessonSentence.lesson_id == lesson_id))
        sentence_list = [
            LessonSentence(lesson_id=lesson.id, sentence=sentence)
            for sentence in request.sentence_list
        ]
        db.add_all(sentence_list)

        lesson.is_public = request.is_public
        lesson.name = request.name
        lesson.description = request.description
        db.add(lesson)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
