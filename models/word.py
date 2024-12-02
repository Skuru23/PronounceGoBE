from typing import Optional

from sqlalchemy import Column, String, Integer
from sqlmodel import Field, SQLModel

from models.base import BaseCreateUpdateModel


class Word(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "words"
    __table_args__ = {
        "comment": "word dictionary",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    word: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True, index=True), default=None
    )
    ipa: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True), default=None
    )
    mean: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    difficult_level: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    path_of_speech: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True), default=None
    )
