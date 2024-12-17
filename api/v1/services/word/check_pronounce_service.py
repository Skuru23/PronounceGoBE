from sqlmodel import Session, select

from models.word import Word
from schemas.word import CheckPronounceRequest


def check_pronounce(db: Session, request: CheckPronounceRequest):
    if " " in request.result_text.strip() or " " in request.expect_text.strip():
        return check_sentence_pronounce(db, request.result_text, request.expect_text)
    else:
        return check_pronounce_word(
            db, request.result_text.lower(), request.expect_text.lower(), 0
        )


def check_pronounce_word(
    db: Session, speech_text: str, result_text: str, start_index: int = 0
):
    speech_text_ipa = get_ipa(db, speech_text)
    result_text_ipa = get_ipa(db, result_text)
    if not result_text_ipa:
        return 0, speech_text_ipa, []

    if "".join(filter(str.isalnum, speech_text)) == "".join(
        filter(str.isalnum, result_text)
    ):
        return 100, result_text_ipa, []

    if not speech_text_ipa:
        return 0, result_text_ipa, []

    accuracy_rate, error_ids = compare_ipa(
        speech_text_ipa, result_text_ipa, start_index
    )

    return (
        int(accuracy_rate * 100),
        f"{result_text_ipa}",
        error_ids,
    )


def get_ipa(db: Session, word: str):
    ipa = db.exec(select(Word.ipa).where(Word.word == word)).first()
    if not ipa and word.endswith("s"):
        ipa = db.exec(select(Word.ipa).where(Word.word == word[:-1])).first()
        if ipa:
            ipa += "s"
    if not ipa and word.endswith("es"):
        ipa = db.exec(select(Word.ipa).where(Word.word == word[:-2])).first()
        if ipa:
            ipa += "ɪz"
    if not ipa and word.endswith("ed"):
        ipa = db.exec(select(Word.ipa).where(Word.word == word[:-2])).first()
        if ipa:
            ipa += "d"
    if not ipa and word.endswith("n't"):
        ipa = db.exec(select(Word.ipa).where(Word.word == word[:-3])).first()
        if ipa:
            ipa += "nt"
    if not ipa and word.endswith("'m"):
        ipa = db.exec(select(Word.ipa).where(Word.word == word[:-2])).first()
        if ipa:
            ipa += "m"
    if not ipa and word.endswith("'s"):
        ipa = db.exec(select(Word.ipa).where(Word.word == word[:-2])).first()
        if ipa:
            ipa += "s"
    return ipa


def compare_ipa(user_ipa: str, target_ipa: str, start_index: int):
    len_user, len_target = len(user_ipa), len(target_ipa)
    min_len = min(len_user, len_target)

    correct_count = 0
    incorrect_positions = []

    for i in range(min_len):
        if user_ipa[i] == target_ipa[i]:
            correct_count += 1
        else:
            incorrect_positions.append(i + start_index)

    # Add remaining characters in target_ipa to incorrect_positions
    if len_target > len_user:
        incorrect_positions.extend(
            range(min_len + start_index, len_target + start_index)
        )

    accuracy_rate = correct_count / max(len_user, len_target)

    return accuracy_rate, incorrect_positions


def check_sentence_pronounce(db: Session, speech_text: str, result_text: str):
    speech_words = speech_text.lower().split()
    expect_words = result_text.lower().split()

    total_score = 0
    total_errors = []
    sentence_ipa = ""
    idx = 0

    for speech_word, expect_word in zip(speech_words, expect_words):
        score, ipa, errors = check_pronounce_word(db, speech_word, expect_word, idx)
        idx += len(ipa) + 1
        total_score += score
        total_errors.extend(errors)
        sentence_ipa = f"{sentence_ipa} {ipa} "

    # Handle remaining words if lengths are different
    if len(speech_words) > len(expect_words):
        for speech_word in speech_words[len(expect_words) :]:
            score, ipa, errors = check_pronounce_word(db, speech_word, "", idx)
            idx += len(ipa) + 1
            total_score += score
            total_errors.extend(errors)
            sentence_ipa = f"{sentence_ipa} {ipa} "
    elif len(expect_words) > len(speech_words):
        for expect_word in expect_words[len(speech_words) :]:
            score, ipa, errors = check_pronounce_word(db, "", expect_word, idx)
            idx += len(ipa) + 1 if ipa else 1
            total_score += score
            total_errors.extend(errors)
            sentence_ipa = f"{sentence_ipa} {ipa} "

    average_score = total_score / max(len(speech_words), len(expect_words))
    return int(average_score), sentence_ipa.strip(), total_errors
