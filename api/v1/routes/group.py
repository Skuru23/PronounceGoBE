from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from api.v1.dependencies.authentication import get_current_user
from core.response import authenticated_api_responses, public_api_responses
from db.database import get_db
from models.user import User
from schemas.group import (
    CreateGroupRequest,
    GetGroupDetailResponse,
    GetGroupMembersResponse,
    GetGroupsQueryParams,
    GetGroupsResponse,
    ListingTopGroupResponse,
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
def listing_group(
    query_params: Annotated[GetGroupsQueryParams, Depends(GetGroupsQueryParams)] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    groups, total = group_services.listing_group(db, user, query_params)
    return GetGroupsResponse(page=1, per_page=10, total=total, data=groups)


@router.get(
    "/top-groups",
    response_model=ListingTopGroupResponse,
    responses=public_api_responses,
)
def listing_top_group(db: Session = Depends(get_db)):
    groups = group_services.listing_top_group(db)

    return ListingTopGroupResponse(data=groups)


@router.get(
    "/{group_id}",
    response_model=GetGroupDetailResponse,
    responses=authenticated_api_responses,
)
def get_group_detail(
    group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return group_services.get_group_detail(db, user, group_id)


@router.patch(
    "/{group_id}/join",
    status_code=HTTPStatus.NO_CONTENT,
    responses=authenticated_api_responses,
)
def join_group(
    group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return group_services.join_group(db, user, group_id)


@router.get(
    "/{group_id}/members",
    response_model=GetGroupMembersResponse,
    responses=authenticated_api_responses,
)
def get_group_members(
    group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    members = group_services.get_group_members(db, user, group_id)

    return GetGroupMembersResponse(data=members)
