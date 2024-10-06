import pandas as pd

dict_file_path = "create_dictionary/dictionary.csv"


def process_vietnamese_analytics(text):
    # Tách loại từ và định nghĩa bằng cách tìm ký tự '|-'
    parts = text.split("|-")
    if len(parts) == 2:
        word_type = parts[0].strip()
        definition = parts[1].strip()
        return word_type, definition
    return None, None


# Hàm đọc và phân tích file CSV bằng Pandas
def analyze_csv_with_pandas(csv_file_path):
    # Đọc file CSV bằng pandas
    df = pd.read_csv(
        csv_file_path, encoding="utf-16", delimiter=",", on_bad_lines="skip"
    )

    results = []

    # Duyệt qua từng dòng trong DataFrame
    for index, row in df.iterrows():
        english_word = row["english"].strip()  # Lấy từ tiếng Anh
        vietnamese_analytics = row["vietnamese_analytics"].strip()

        # Xử lý thông tin trong cột vietnamese_analytics
        word_type, definition = process_vietnamese_analytics(vietnamese_analytics)

        # Thêm kết quả vào danh sách nếu tách thành công
        if word_type and definition:
            results.append(
                {
                    "english_word": english_word,
                    "word_type": word_type,
                    "definition": definition,
                }
            )

    return results


# Ví dụ sử dụng hàm với đường dẫn tới file CSV
results = analyze_csv_with_pandas(dict_file_path)

# Hiển thị kết quả phân tích
for result in results:
    print(f"Từ tiếng Anh: {result['english_word']}")
    print(f"Loại từ: {result['word_type']}")
    print(f"Định nghĩa: {result['definition']}")
    print("-" * 50)
