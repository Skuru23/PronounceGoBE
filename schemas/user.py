from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.user import RoleCode


class UserBase(BaseModel):
    id: Optional[int]
    role_code: Optional[RoleCode]
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
