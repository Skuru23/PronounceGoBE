from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, String, Integer
from sqlmodel import Field, SQLModel

from models.base import BaseCreateUpdateModel


class GroupMember(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "group_members"
    __table_args__ = {
        "comment": "group_members",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    user_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True), default=None
    )
    is_manager: Optional[int] = Field(
        sa_column=Column(Boolean, nullable=True), default=False
    )
    approved_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=True,
        ),
        default=None,
    )
