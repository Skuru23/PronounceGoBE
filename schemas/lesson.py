from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field


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
    word_ids: List[int] = Field(default=[])
    sentence_list: List[str] = Field(default=[])
