from passlib.context import CryptContext

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
        return "Dễ"
    elif ipa_length <= 10 and syllable_count <= 2 and total_complex_vowels <= 1:
        return "Trung bình"
    else:
        return "Khó"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
