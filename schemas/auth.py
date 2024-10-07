from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


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
