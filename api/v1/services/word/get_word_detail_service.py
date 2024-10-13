from sqlmodel import Session, select

from core.exception import BadRequestException, ErrorCode, ErrorMessage
from models.word import Word


def get_word_detail(db: Session, word_id: int):
    word = db.exec(select(Word).where(Word.id == word_id)).one_or_none()
    if not word_id:
        raise BadRequestException(
            ErrorCode.ERR_WORD_NOT_FOUND, ErrorMessage.ERR_WORD_NOT_FOUND
        )

    return word
