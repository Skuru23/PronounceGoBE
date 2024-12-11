from typing import Optional
from pydantic import BaseModel

from models.progress_word import ItemStatus


class ProgressSentenceBase(BaseModel):
    id: int
    progress_id: int
    item_id: int
    status: Optional[ItemStatus]


class ProgressSentenceDetailItem(ProgressSentenceBase):
    sentence: str
