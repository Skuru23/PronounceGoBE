from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Field

from schemas.lesson_sentence import LessonSentenceBase
from schemas.word import WordBase


class LessonBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    user_owner_id: Optional[int]
    group_owner_id: Optional[int]
    is_public: Optional[bool]


class CreatePersonLessonRequest(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    is_public: bool
    group_owner_id: Optional[int] = Field(default=None)
    word_ids: List[int] = Field(default=[])
    sentence_list: List[str] = Field(default=[])
    image_path: Optional[str] = Field(default=None)


class GetLessonQuery(BaseModel):
    is_public: Optional[bool] = Field(Query(None))
    user_owner_id: Optional[str] = Field(Query(None))
    group_owner_id: Optional[str] = Field(Query(None))
    keyword: Optional[str] = Field(Query(None))


class ListLessonsItem(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    user_owner_id: Optional[int]
    group_owner_id: Optional[int]
    is_public: Optional[bool]
    total_likes: Optional[int]
    total_learners: Optional[int]
    creator: Optional[str]


class ListLessonsResponse(BaseModel):
    data: List[ListLessonsItem] = []


class GetLessonDetailResponse(LessonBase):
    word_list: Optional[List[WordBase]] = Field(default=[])
    sentence_list: Optional[List[LessonSentenceBase]] = Field(default=[])


class UpdateLessonRequest(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    is_public: bool
    word_ids: List[int] = Field(default=[])
    sentence_list: List[str] = Field(default=[])
