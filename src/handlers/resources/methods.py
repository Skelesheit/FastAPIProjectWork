from fastapi import APIRouter, Depends, Path, Query
from typing import List

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import MethodCreate, MethodUpdate, MethodOut
from src.services.resources.method_service import MethodService

router = APIRouter(
    prefix="/methods",
    tags=["methods"]
)


@router.get("/", response_model=List[MethodOut])
async def get_methods(
    enterprise_id: int = Depends(get_enterprise_by_user_id),
    name: str | None = Query(default=None),
):
    return await MethodService.list(enterprise_id, name=name)


@router.post("/", response_model=MethodOut)
async def create_method(
    payload: MethodCreate,
    enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MethodService.create(payload, enterprise_id)


@router.get("/{method_id}", response_model=MethodOut)
async def get_method_by_id(
    method_id: int = Path(...),
    enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MethodService.get(method_id, enterprise_id)


@router.put("/{method_id}", response_model=MethodOut)
async def update_method(
    payload: MethodUpdate,
    method_id: int = Path(...),
    enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MethodService.update(method_id, payload, enterprise_id)


@router.delete("/{method_id}", response_model=bool)
async def delete_method(
    method_id: int = Path(...),
    enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MethodService.delete(method_id, enterprise_id)
