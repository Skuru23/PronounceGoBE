from typing import Optional
from pydantic import BaseModel

from models.progress_word import ItemStatus


class ProgressWordBase(BaseModel):
    id: int
    progress_id: int
    item_id: int
    status: Optional[ItemStatus]


class ProgressWordDetailItem(ProgressWordBase):
    word_id: int
    word: str
    ipa: Optional[str]
