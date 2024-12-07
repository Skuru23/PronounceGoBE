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
