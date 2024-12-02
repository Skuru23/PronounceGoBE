from pydantic import BaseModel


class LearnWordResponse(BaseModel):
    text: str
    ipa: str
    error: list[int]
    point: int


class LearnWordRequest(BaseModel):
    speech_text: str


class LearnSentenceResponse(BaseModel):
    text: str
    ipa: str
    error: list[int]
    point: int


class LearnSentenceRequest(BaseModel):
    speech_text: str
