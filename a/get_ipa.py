import requests
from sqlalchemy import update
from sqlmodel import select
from db.database import get_db
from models.word import Word

db = next(get_db())
url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

words = db.exec(select(Word).where(Word.id >= 0).where(Word.id < 1000)).all()

for word in words:
    # print(f"{url}{word.word}")

    response = requests.get(f"{url}{word.word}")

    if response.status_code == 200:
        data = response.json()
        phonetic = data[0].get("phonetic", None)
        if phonetic:
            print(f"{word.word}: {phonetic}")
            word.ipa = phonetic

# db.add_all(words)
db.commit()
