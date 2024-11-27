from typing import Optional
from sqlalchemy import Column, Enum, Integer
from sqlmodel import Field, SQLModel
from models.base import BaseCreateUpdateModel

from models.progress_word import ItemStatus


class ProgressSentence(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "progress_sentences"

    id: Optional[int] = Field(default=None, primary_key=True)
    progress_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    item_id: Optional[str] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    status: Optional[ItemStatus] = Field(
        sa_column=Column(Enum(ItemStatus), nullable=True), default=None
    )
