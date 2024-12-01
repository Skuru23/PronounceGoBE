from sqlmodel import Session, select
from core.exception import BadRequestException, ErrorCode
from models.group_member import GroupMember
from models.lesson import Lesson
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.progress import Progress
from models.progress_word import ItemStatus, ProgressWord
from models.user import User


def learn_lesson(db: Session, user: User, lesson_id: int):
    lesson = db.exec(select(Lesson).where(Lesson.id == lesson_id)).first()

    if lesson.user_owner_id != user.id:
        if not lesson.group_owner_id:
            raise BadRequestException(error_code=ErrorCode.ERR_ACCESS_DENIED)

        is_member = db.exec(
            select(GroupMember)
            .where(GroupMember.group_id == lesson.group_owner_id)
            .where(GroupMember.user_id == user.id)
        ).first()

        if not is_member:
            if not lesson.group_owner_id:
                raise BadRequestException(error_code=ErrorCode.ERR_ACCESS_DENIED)
    try:
        progress = Progress(user_id=user.id, lesson_id=lesson_id)
        db.add(progress)
        db.flush()

        lesson_words = db.exec(
            select(LessonWord).where(LessonWord.lesson_id == lesson_id)
        ).all()
        progress_word = [
            ProgressWord(
                progress_id=progress.id, item_id=item.id, status=ItemStatus.NOT_STARTED
            )
            for item in lesson_words
        ]
        db.add_all(progress_word)

        lesson_sentences = db.exec(
            select(LessonSentence).where(LessonSentence.lesson_id == lesson_id)
        ).all()
        progress_sentences = [
            ProgressWord(
                progress_id=progress.id, item_id=item.id, status=ItemStatus.NOT_STARTED
            )
            for item in lesson_sentences
        ]
        db.add_all(progress_sentences)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
