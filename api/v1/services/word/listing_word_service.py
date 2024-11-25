from sqlmodel import Session, select
from models.word import Word
from schemas.word import ListingWordRequest


def listing_words(db: Session, request: ListingWordRequest):

    query = select(
        Word.id,
        Word.word,
        Word.ipa,
        Word.mean,
        Word.difficult_level,
        Word.path_of_speech,
    ).limit(int(request.total) if request.total else 20)

    if request.keyword:
        query = query.where(Word.word.startswith(request.keyword))
    if request.difficult_level:
        query = query.where(Word.difficult_level == int(request.difficult_level))

    words = db.exec(query).mappings().all()

    return words
