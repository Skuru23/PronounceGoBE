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


class CheckPronounceResponse(BaseModel):
    text: str
    ipa: str
    error: list[int]
    point: int


class CheckPronounceRequest(BaseModel):
    result_text: str
    expect_text: str
