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
    image_path: Optional[str]


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
    image_path: Optional[str]
    is_public: Optional[bool]
    is_liked: Optional[bool]
    total_likes: Optional[int]
    total_learners: Optional[int]
    creator: Optional[str]


class ListLessonsResponse(BaseModel):
    data: List[ListLessonsItem] = []


class GetLessonDetailResponse(LessonBase):
    creator_name: Optional[str] = Field(None, description="Name of the creator")
    is_in_progress: Optional[bool] = Field(None, description="Is lesson in progress")
    is_liked: Optional[bool] = Field(None, description="Is lesson liked")
    group_owner_name: Optional[str] = Field(None, description="Name of the group owner")
    words: List[WordBase] = Field([], description="List of words in the lesson")
    sentences: List[LessonSentenceBase] = Field(
        [], description="List of sentences in the lesson"
    )


class UpdateLessonRequest(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    is_public: bool
    word_ids: List[int] = Field(default=[])
    sentence_list: List[str] = Field(default=[])


class LearnLessonResponse(BaseModel):
    progress: int
