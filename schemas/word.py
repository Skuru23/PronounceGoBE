from typing import Optional
from pydantic import BaseModel


class WordBase(BaseModel):
    id: Optional[int]
    word: Optional[str]
    ipa: Optional[str]
    mean: Optional[str]
    difficult_level: Optional[int]
    path_of_speech: Optional[str]


class WordDetailResponse(WordBase):
    pass
