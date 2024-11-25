from typing import Annotated, Optional
from fastapi import Query
from pydantic import BaseModel, Field, root_validator


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


class ListingWordRequest(BaseModel):
    keyword: Optional[str] = Field(Query(default=None))
    total: Optional[str] = Field(Query(default="20"))
    difficult_level: Annotated[Optional[str], Field(Query(default=None))]

    @root_validator(pre=True)
    def convert_empty_strings_to_none(cls, values):
        # Kiểm tra và thay đổi giá trị nếu cần
        for field in ["total", "difficult_level"]:
            if values.get(field) == "":
                values[field] = None
        return values


class ListingWordResponse(BaseModel):
    data: list[WordBase]
