from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, SQLModel
from models.base import BaseCreateUpdateModel


class LessonWord(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "lesson_words"

    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    word_id: Optional[str] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
