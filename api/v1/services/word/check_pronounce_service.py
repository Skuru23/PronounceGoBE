from sqlmodel import Session, select

from models.word import Word
from schemas.word import CheckPronounceRequest


def check_pronounce(db: Session, request: CheckPronounceRequest):
    score, ipa, errors = check_pronounce_word(
        db, request.result_text.lower(), request.expect_text.lower()
    )
    return int(score * 100), ipa, errors


def check_pronounce_word(db: Session, speech_text: str, result_text: str):

    speech_text_ipa = db.exec(select(Word.ipa).where(Word.word == speech_text)).first()

    if speech_text == result_text:
        return 1, speech_text_ipa, []

    result_text_ipa = db.exec(select(Word.ipa).where(Word.word == result_text)).first()

    if (not speech_text_ipa) or (not result_text_ipa):
        return 1, speech_text_ipa, []

    accuracy_rate, error_ids = compare_ipa(speech_text_ipa, result_text_ipa)

    return accuracy_rate, f"{result_text_ipa} -- {speech_text_ipa}", error_ids
    # for char in result_text_ipa:


def compare_ipa(user_ipa: str, target_ipa: str):
    len_user, len_target = len(user_ipa), len(target_ipa)
    min_len = min(len_user, len_target)

    correct_count = 0
    incorrect_positions = []

    for i in range(min_len):
        if user_ipa[i] == target_ipa[i]:
            correct_count += 1
        else:
            incorrect_positions.append(i)

    accuracy_rate = correct_count / max(len_user, len_target)

    if incorrect_positions:
        return accuracy_rate, incorrect_positions
    else:
        return accuracy_rate, []
