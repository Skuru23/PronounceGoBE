from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from api.v1.dependencies.authentication import get_current_user
from api.v1.services import image as image_services
from models.user import User

router = APIRouter()


@router.post("/upload")
def upload_image(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    return image_services.upload_image(file, user)


@router.get("/get/{image_name}")
def get_image(image_name: str):
    if image_name:
        image_path = f"images/{image_name}"
    return FileResponse(image_path)
