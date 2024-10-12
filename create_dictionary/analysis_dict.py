import pandas as pd
import re

dict_file_path = "create_dictionary/cleaned_dict.csv"

TYPE_MAP = {
    "danh từ": "N",  # Noun
    "phó từ": "ADV",  # Adverb
    "tính từ": "ADJ",  # Adjective
    "ngoại động từ": "V",  # Transitive verb
    "nội động từ": "V",  # Intransitive verb
    "giới từ": "P",  # Preposition
    "liên từ": "CONJ",  # Conjunction
    "đại từ": "PRON",  # Pronoun
    "từ hạn định": "DET",  # Determiner
    "thán từ": "INT",  # Interjection
    "trạng từ": "ADV",  # Adverb (alternative)
    "động từ": "V",  # Verb (general)
    "cụm danh từ": "NP",  # Noun Phrase
    "cụm động từ": "VP",  # Verb Phrase
}


def extract_ipa(text):
    match = re.search(r"\[(.*?)\]", text)
    if match:
        ipa = match.group(1)
        keyword = re.sub(r"\s*\[.*?\]\s*", "", text).strip()
        return ipa, keyword[:64]
    return None, text.strip()[:64]


def process_vietnamese_analytics(text):
    parts = text.split("|-", 1)
    if len(parts) == 2:
        word_type = parts[0].strip()
        definition = parts[1].strip()

        for key in TYPE_MAP:
            if key in word_type:
                return TYPE_MAP[key], definition[:2000]

    return "OTHER", text.strip()[:2000]


DIPHTHONGS = ["aɪ", "eɪ", "ɔɪ", "aʊ", "oʊ", "ɪə", "eə", "ʊə"]
TRIPHTHONGS = ["aɪə", "aʊə", "eɪə", "ɔɪə", "oʊə"]


def analyze_ipa_difficulty(ipa: str) -> str:
    """
    Hàm phân tích độ khó của phiên âm IPA dựa trên:
    1. Độ dài phiên âm (số ký tự)
    2. Số lượng âm tiết (khoảng trống phân cách giữa các âm tiết)
    3. Nguyên âm đôi (diphthong) và nguyên âm ba (triphthong)

    Trả về: Chuỗi mô tả độ khó ("Dễ", "Trung bình", "Khó")
    """

    # 1. Độ dài phiên âm
    ipa_length = len(ipa)

    # 2. Số lượng âm tiết (tính bằng cách đếm số khoảng trắng)
    syllable_count = ipa.count(" ") + 1  # Mỗi khoảng trắng ngăn cách âm tiết

    # 3. Đếm số nguyên âm đôi và nguyên âm ba trong phiên âm
    diphthong_count = sum(ipa.count(dip) for dip in DIPHTHONGS)
    triphthong_count = sum(ipa.count(tri) for tri in TRIPHTHONGS)

    # Tính tổng số nguyên âm đôi và ba
    total_complex_vowels = diphthong_count + triphthong_count

    # Phân loại độ khó dựa trên các tiêu chí
    if ipa_length <= 5 and syllable_count == 1 and total_complex_vowels == 0:
        return 1
    elif ipa_length <= 10 and syllable_count <= 2 and total_complex_vowels <= 1:
        return 2
    else:
        return 3


def analyze_csv_with_pandas(csv_file_path):
    df = pd.read_csv(
        csv_file_path, encoding="utf-8", delimiter="+", on_bad_lines="skip"
    )

    results = []

    for index, row in df.iterrows():
        try:
            english_word = row["english"].strip()
            vietnamese_analytics = row["vietnamese_analytics"].strip()

            word_type, definition = process_vietnamese_analytics(vietnamese_analytics)

            ipa, word = extract_ipa(english_word)

            if ipa:
                results.append(
                    {
                        "english_word": word,
                        "word_type": word_type,
                        "definition": definition,
                        "ipa": ipa,
                        "difficult_level": analyze_ipa_difficulty(ipa),
                    }
                )

        except Exception as e:
            print(f"{index}, : {e}")
            break

    return results


results = analyze_csv_with_pandas(dict_file_path)

df = pd.DataFrame(results)
df.to_csv("create_dictionary/final_dict.csv", index=False)
