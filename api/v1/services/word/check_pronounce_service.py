from sqlalchemy import func
from sqlmodel import Session, select

from models.word import Word
from schemas.word import CheckPronounceRequest
import numpy as np


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
    print(speech_text_ipa, result_text_ipa)
    if "".join(filter(str.isalnum, speech_text)) == "".join(
        filter(str.isalnum, result_text)
    ):
        if not result_text_ipa:
            return 100, "", []

        return 100, result_text_ipa, []

    if not speech_text_ipa and not result_text_ipa:
        print("Not found")
        return 0, "", []

    if not speech_text_ipa:
        return 0, result_text_ipa, []

    if not result_text_ipa:
        return 0, speech_text_ipa, []

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
    if not ipa:
        ipa = db.exec(select(Word.word).where(Word.word.like(word)).limit(1)).first()
    return ipa


def compare_ipa(ipa_standard: str, ipa_user: str, start_index: int):
    ipa_standard = ipa_standard.strip() if ipa_standard else ""
    ipa_user = ipa_user.strip() if ipa_user else ""

    len_std, len_usr = len(ipa_standard), len(ipa_user)
    dp = np.zeros((len_std + 1, len_usr + 1), dtype=int)
    trace = np.zeros((len_std + 1, len_usr + 1), dtype=object)

    for i in range(len_std + 1):
        dp[i][0] = i
        trace[i][0] = ("delete", i - 1)
    for j in range(len_usr + 1):
        dp[0][j] = j
        trace[0][j] = ("insert", j - 1)

    for i in range(1, len_std + 1):
        for j in range(1, len_usr + 1):
            if ipa_standard[i - 1] == ipa_user[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                trace[i][j] = ("match", i - 1, j - 1)
            else:
                delete_cost = dp[i - 1][j] + 1
                insert_cost = dp[i][j - 1] + 1
                replace_cost = dp[i - 1][j - 1] + 1

                min_cost = min(delete_cost, insert_cost, replace_cost)
                dp[i][j] = min_cost

                if min_cost == delete_cost:
                    trace[i][j] = ("delete", i - 1)
                elif min_cost == insert_cost:
                    trace[i][j] = ("insert", j - 1)
                else:
                    trace[i][j] = ("replace", i - 1, j - 1)

    error_positions = []
    i, j = len_std, len_usr
    while i > 0 or j > 0:
        action = trace[i][j][0]
        if action == "match":
            i, j = trace[i][j][1], trace[i][j][2]
        elif action == "replace":
            error_positions.append(start_index + trace[i][j][1])
            i, j = trace[i][j][1], trace[i][j][2]
        elif action == "delete":
            error_positions.append(start_index + trace[i][j][1])
            i -= 1
        elif action == "insert":
            j -= 1

    max_len = len_std
    score = max(0, (1 - dp[len_std][len_usr] / max_len))

    return round(score, 2), list(reversed(error_positions))


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
