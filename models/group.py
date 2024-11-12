from typing import Optional

from sqlalchemy import Boolean, Column, Enum, String, Integer
from sqlmodel import Field, SQLModel

from models.base import BaseCreateUpdateModel


class Group(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "groups"
    __table_args__ = {
        "comment": "groups",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True), default=None
    )
    description: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    owner_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
