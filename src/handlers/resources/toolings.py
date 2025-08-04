# src/handlers/resources/tooling_router.py

from typing import List

from fastapi import APIRouter, Depends, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import ToolingCreate, ToolingUpdate, ToolingOut
from src.services.resources.tooling_service import ToolingService

router = APIRouter(
    prefix="/toolings",
    tags=["toolings"]
)


@router.get('', response_model=List[ToolingOut])
async def list_toolings(
    enterprise_id: int = Depends(get_enterprise_by_user_id),
    name: str | None = Query(None),
):
    return await ToolingService.list(enterprise_id=enterprise_id, name=name)


@router.post('', response_model=ToolingOut)
async def create_tooling(
    payload: ToolingCreate,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolingService.create(enterprise_id=enterprise_id, **payload.model_dump())


@router.get('/{tooling_id}', response_model=ToolingOut)
async def get_tooling_by_id(
    tooling_id: int,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolingService.get(tooling_id, enterprise_id)


@router.put('/{tooling_id}', response_model=ToolingOut)
async def update_tooling(
    tooling_id: int,
    payload: ToolingUpdate,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolingService.update(tooling_id, enterprise_id, **payload.model_dump())


@router.delete('/{tooling_id}')
async def delete_tooling(
    tooling_id: int,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolingService.delete(tooling_id, enterprise_id)
