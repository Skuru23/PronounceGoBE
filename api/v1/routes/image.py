from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from api.v1.dependencies.authentication import get_current_user
from api.v1.services import image as image_services
from models.user import User
from schemas.image import UploadImageResponse

router = APIRouter()


@router.post("/upload", response_model=UploadImageResponse)
def upload_image(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    path = image_services.upload_image(file, user)
    return UploadImageResponse(path=path)


@router.get("/{image_name}", include_in_schema=False)
def get_image(image_name: str):
    if image_name:
        image_path = f"images/{image_name}"
    return FileResponse(image_path)
