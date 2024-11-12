from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses
from db.databse import get_db
from models.user import User
from schemas.group import (
    CreateGroupRequest,
    GetGroupsQueryParams,
    GetGroupsResponse,
)
from api.v1.services import group as group_services

router = APIRouter()


@router.post(
    "", status_code=HTTPStatus.NO_CONTENT, responses=authenticated_api_responses
)
def create_group(
    request: CreateGroupRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    group_services.create_group(db, user, request)


@router.get("", response_model=GetGroupsResponse, responses=authenticated_api_responses)
def create_group(
    query_params: Annotated[GetGroupsQueryParams, Depends(GetGroupsQueryParams)] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    groups, total = group_services.listing_group(db, query_params)

    return GetGroupsResponse(
        page=query_params.page, per_page=query_params.per_page, total=total, data=groups
    )
