from typing import Optional
from sqlalchemy import Column, Enum, Integer, String
from sqlmodel import Field, SQLModel
from models.base import BaseCreateUpdateModel
import enum


class ItemStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class ProgressWord(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "progress_words"

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
