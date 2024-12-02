from sqlmodel import Session, select
from api.v1.services.word.check_pronounce_service import check_sentence_pronounce
from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.lesson_sentence import LessonSentence
from models.lesson_word import LessonWord
from models.progress import Progress
from models.progress_sentence import ProgressSentence
from models.progress_word import ItemStatus, ProgressWord
from models.user import User
from models.word import Word
from schemas.learn import LearnSentenceResponse, LearnWordResponse


def learn_sentence(
    db: Session, user: User, progress_sentence_id: int, speech_text: str
):
    progress_sentence = db.exec(
        select(ProgressSentence).where(ProgressSentence.id == progress_sentence_id)
    ).first()
    if not progress_sentence:
        raise BadRequestException(
            ErrorCode.ERR_PROGRESS_SENTENCE_NOT_FOUND,
            ErrorMessage.ERR_PROGRESS_SENTENCE_NOT_FOUND,
        )
    progress = db.exec(
        select(Progress).where(Progress.id == progress_sentence.progress_id)
    ).first()
    if not progress:
        raise BadRequestException(
            ErrorCode.ERR_PROGRESS_NOT_FOUND, ErrorMessage.ERR_PROGRESS_NOT_FOUND
        )
    if progress.user_id != user.id:
        raise BadRequestException(
            ErrorCode.ERR_ACCESS_DENIED, ErrorMessage.ERR_ACCESS_DENIED
        )

    sentence = db.exec(
        select(LessonSentence.sentence).where(
            LessonSentence.id == ProgressSentence.item_id
        )
    ).first()
    if not sentence:
        raise BadRequestException(
            ErrorCode.ERR_WORD_NOT_FOUND, ErrorMessage.ERR_WORD_NOT_FOUND
        )
    accuracy_rate, result_text_ipa, error_ids = check_sentence_pronounce(
        db, speech_text, sentence
    )

    if accuracy_rate == 100:
        progress_sentence.status = ItemStatus.DONE
    else:
        progress_sentence.status = ItemStatus.IN_PROGRESS
    db.add(progress_sentence)
    db.commit()

    return LearnSentenceResponse(
        text=sentence,
        ipa=result_text_ipa,
        error=error_ids,
        point=accuracy_rate,
    )
