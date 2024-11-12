from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, SQLModel
from models.base import BaseCreateUpdateModel


class LessonSentence(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "lesson_sentences"

    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    sentence: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
