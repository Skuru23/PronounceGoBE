from sqlmodel import Session

from models.user import User
from schemas.user import UpdateUserRequest
import shutil
import os


def update_information(db: Session, user: User, request: UpdateUserRequest):
    # Move current image to /images/tmp if it exists
    if user.image_path:
        tmp_dir = "/images/tmp"
        os.makedirs(tmp_dir, exist_ok=True)
        new_image_path = os.path.join(tmp_dir, os.path.basename(user.image_path))
        shutil.move(user.image_path, new_image_path)
        user.image_path = new_image_path

    user.name = request.name
    user.phone = request.phone
    user.address = request.address
    user.image_path = request.image_path
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
