from typing import Optional

from sqlalchemy import Boolean, Column, Integer
from sqlmodel import Field, SQLModel

from models.base import BaseCreateUpdateModel


class LessonLike(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "lesson_likes"
    __table_args__ = {
        "comment": "This table is for storing likes for lessons.",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    user_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
