import uuid
from fastapi import UploadFile
from core.config import settings
from models.user import User
import datetime


def upload_image(file: UploadFile, user: User):
    allowed_content_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

    if file.content_type not in allowed_content_types:
        raise ValueError(
            "Invalid file type. Only JPEG, PNG, JPG, and WEBP files are allowed."
        )

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    extension = file.filename.split(".")[-1]
    file.filename = f"{timestamp}_{user.name}.{extension}"

    content = file.file.read()

    with open(f"{settings.IMG_DIR}/{file.filename}", "wb") as f:
        f.write(content)

    return f"{settings.IMG_DIR}/{file.filename}"
