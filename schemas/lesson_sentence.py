from typing import Optional
from pydantic import BaseModel, Field


class LessonSentenceBase(BaseModel):
    id: Optional[int] = Field(default=None)
    sentence: Optional[str] = Field(default=None)
