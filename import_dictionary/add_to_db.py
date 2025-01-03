import pandas as pd
from db.database import get_db

from models.word import Word


def add_to_db(file_path: str):
    try:
        db = next(get_db())
        df = pd.read_csv(file_path)

        # Xử lý từng mảng 1000 ký tự
        total_rows = len(df)
        for start in range(0, total_rows, 1000):
            end = start + 1000
            batch = df[start:end]

            words = []
            for index, row in batch.iterrows():
                try:
                    word = Word(
                        word=row["english_word"],
                        path_of_speech=row["word_type"],
                        mean=row["definition"],
                        ipa=row["ipa"],
                        difficult_level=row["difficult_level"],
                    )
                    words.append(word)
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")

            # Lưu vào cơ sở dữ liệu
            db.add_all(words)
            db.commit()

            print(f"Processed rows {start + 1} to {min(end, total_rows)}.")

    except Exception as e:
        print(f"Error reading the CSV file: {e}")


add_to_db("create_dictionary/final_dict.csv")
