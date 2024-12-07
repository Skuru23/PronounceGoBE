from typing import Optional

from sqlalchemy import Boolean, Column, Enum, String, Integer
from sqlmodel import Field, SQLModel

from models.base import BaseCreateUpdateModel

# class LessonType(str, enum.Enum):
#     PRIVATE = "PRIVATE"
#     PUBLIC = "PUBLIC"


class Lesson(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "lessons"
    __table_args__ = {
        "comment": "lesson",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True), default=None
    )
    description: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    # role_code: Optional[LessonType] = Field(sa_column=Column(Enum(LessonType)))
    user_owner_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    group_owner_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    is_public: Optional[bool] = Field(
        sa_column=Column(Boolean, nullable=True), default=None
    )
    image_path: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
