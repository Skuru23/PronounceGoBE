from datetime import datetime
from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[int]
    image_path: Optional[str] = None


class CreateGroupRequest(BaseModel):
    name: str
    description: str
    image_path: Optional[str] = None


class GetGroupItem(GroupBase):
    creator: str
    total_member: int = Field(default=0)
    total_lesson: int = Field(default=0)
    total_like: int = Field(default=0)
    is_member: Optional[bool] = None


class GetGroupsResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: List[GetGroupItem]


class GetGroupsQueryParams(BaseModel):
    # page: Optional[int] = Query(default=1)
    # per_page: Optional[int] = Query(default=10)
    name: Optional[str] = Query(default=None)
    is_member: Optional[str] = Query(default=None)
    sort_by: Optional[str] = Query(default=None)


class GetGroupDetailResponse(GroupBase):
    creator: str
    total_member: int = Field(default=0)
    total_lesson: int = Field(default=0)
    total_like: int = Field(default=0)
    is_member: Optional[bool] = None
    is_owner: Optional[bool] = None


class GroupMemberItem(BaseModel):
    id: int
    user_id: int
    name: Optional[str]
    is_manager: bool
    approved_at: Optional[datetime] = None


class GetGroupMembersResponse(BaseModel):
    data: List[GroupMemberItem] = Field(default=[])


class ListingTopGroupResponse(BaseModel):
    data: List[GroupBase] = Field(default=[])
