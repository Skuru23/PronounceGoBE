from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    path: str
