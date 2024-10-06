from fastapi import APIRouter

from api.v1.routes import router

routers = APIRouter()

routers.include_router(router)

