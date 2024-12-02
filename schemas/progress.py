from typing import List, Optional
from pydantic import BaseModel, Field


class ProgressBase(BaseModel):
    id: int
    lesson_id: int


class ListingProgressItem(ProgressBase):
    lesson_name: Optional[str]
    total_word: Optional[int] = Field(default=0)
    remain_word: Optional[int] = Field(default=0)
    total_sentence: Optional[int] = Field(default=0)
    remain_sentence: Optional[int] = Field(default=0)
    finish_percent: Optional[int] = Field(default=0)


class ListingProgressResponse(BaseModel):
    data: Optional[List[ListingProgressItem]] = Field(default=None)


class ProgressDetailResponse(ProgressBase):
    lesson_name: Optional[str]
    creator_name: Optional[str]
    group_owner_name: Optional[str]
    total_word: Optional[int] = Field(default=0)
    remain_word: Optional[int] = Field(default=0)
    total_sentence: Optional[int] = Field(default=0)
    remain_sentence: Optional[int] = Field(default=0)
    finish_percent: Optional[int] = Field(default=0)
