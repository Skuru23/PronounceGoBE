from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

from schemas.user import UserBase


class LoginResponse(BaseModel):
    id: int


class SignupRequest(BaseModel):
    email: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    phone: Annotated[str, Field(...)]
    address: Annotated[str, Field(...)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token_type: str
    access_token: str
    expire_at: datetime
    refresh_token: str
    refresh_expire_at: datetime


class GetMeResponse(UserBase):
    pass
