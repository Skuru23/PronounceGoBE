from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[int]


class CreateGroupRequest(BaseModel):
    name: str
    description: str


class GetGroupItem(GroupBase):
    creator: str
    total_member: int = Field(default=0)
    total_lesson: int = Field(default=0)
    total_like: int = Field(default=0)


class GetGroupsResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: List[GetGroupItem]


class GetGroupsQueryParams(BaseModel):
    # page: Optional[int] = Query(default=1)
    # per_page: Optional[int] = Query(default=10)
    name: Optional[str] = Query(default=None)
    sort_by: Optional[str] = Query(default=None)
