from sqlmodel import Session, select
from api.v1.services.word.check_pronounce_service import check_pronounce_word
from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.lesson_word import LessonWord
from models.progress import Progress
from models.progress_word import ItemStatus, ProgressWord
from models.user import User
from models.word import Word
from schemas.learn import LearnWordResponse


def learn_word(db: Session, user: User, progress_word_id: int, speech_text: str):
    progress_word = db.exec(
        select(ProgressWord).where(ProgressWord.id == progress_word_id)
    ).first()
    if not progress_word:
        raise BadRequestException(
            ErrorCode.ERR_PROGRESS_WORD_NOT_FOUND,
            ErrorMessage.ERR_PROGRESS_WORD_NOT_FOUND,
        )
    progress = db.exec(
        select(Progress).where(Progress.id == progress_word.progress_id)
    ).first()
    if not progress:
        raise BadRequestException(
            ErrorCode.ERR_PROGRESS_NOT_FOUND, ErrorMessage.ERR_PROGRESS_NOT_FOUND
        )
    if progress.user_id != user.id:
        raise BadRequestException(
            ErrorCode.ERR_ACCESS_DENIED, ErrorMessage.ERR_ACCESS_DENIED
        )

    word = db.exec(
        select(Word)
        .join(LessonWord, LessonWord.word_id == Word.id)
        .where(LessonWord.id == progress_word.item_id)
    ).first()
    if not word:
        raise BadRequestException(
            ErrorCode.ERR_WORD_NOT_FOUND, ErrorMessage.ERR_WORD_NOT_FOUND
        )

    print(word.word)
    accuracy_rate, result_text_ipa, error_ids = check_pronounce_word(
        db, speech_text, word.word
    )

    if accuracy_rate == 100:
        progress_word.status = ItemStatus.DONE
    else:
        progress_word.status = ItemStatus.IN_PROGRESS
    db.add(progress_word)
    db.commit()

    return LearnWordResponse(
        text=word.word,
        ipa=result_text_ipa,
        error=error_ids,
        point=accuracy_rate,
    )
