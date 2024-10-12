import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import routers
from core.response import BadRequestResponse, AccessDeniedResponse, UnauthorizedResponse
from core.exception import (
    BadRequestException,
    AccessDeniedException,
    UnauthorizedException,
)

app = FastAPI(title="FAST API", openapi_url="/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["content-disposition"],
)


os.environ["TZ"] = "Asia/Ho_Chi_Minh"

app.include_router(routers, prefix="/api/v1")


@app.exception_handler(BadRequestException)
def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return BadRequestResponse(exc.error_code, exc.message, exc.debug_info)


@app.exception_handler(UnauthorizedException)
def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return UnauthorizedResponse(exc.error_code, exc.message, exc.debug_info)


@app.exception_handler(AccessDeniedException)
def access_denied_exception_handler(request: Request, exc: UnauthorizedException):
    return AccessDeniedResponse(exc.error_code, exc.message, exc.debug_info)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return BadRequestResponse(400, str(exc))
