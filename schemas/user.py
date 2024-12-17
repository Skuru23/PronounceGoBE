from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from models.user import RoleCode


class UserBase(BaseModel):
    id: Optional[int]
    role_code: Optional[RoleCode]
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    image_path: Optional[str] = Field(None, description="imagePath")


class UpdateUserRequest(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    image_path: Optional[str] = Field(None, description="imagePath")


class UserResponse(UserBase):
    total_progress: Optional[int] = Field(default=0)
    remain_progress: Optional[int] = Field(default=0)
    done_progress: Optional[int] = Field(default=0)
    not_start_progress: Optional[int] = Field(default=0)
    total_lesson: Optional[int] = Field(default=0)
    joined_group: Optional[int] = Field(default=0)
