from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, SQLModel
from models.base import BaseCreateUpdateModel


class Progress(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "progresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    lesson_id: Optional[str] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
