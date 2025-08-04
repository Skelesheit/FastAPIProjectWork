from typing import List

from fastapi import APIRouter, Depends, Path, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import OperationTypeCreate, OperationTypeUpdate, OperationTypeOut
from src.services.resources.operation_type_service import OperationTypeService

router = APIRouter(
    prefix="/operation-types",
    tags=["operation-types"]
)


@router.get('', response_model=List[OperationTypeOut])
async def get_operation_types(
        name: str | None = Query(default=None),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await OperationTypeService.list(enterprise_id, name=name)


@router.post('', response_model=OperationTypeOut)
async def create_operation_type(
        payload: OperationTypeCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await OperationTypeService.create(payload, enterprise_id)


@router.get('/{type_id}', response_model=OperationTypeOut)
async def get_operation_type_by_id(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await OperationTypeService.get(type_id, enterprise_id)


@router.put('/{type_id}', response_model=OperationTypeOut)
async def update_operation_type(
        type_id: int = Path(...),
        payload: OperationTypeUpdate = ...,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await OperationTypeService.update(type_id, payload, enterprise_id)


@router.delete('/{type_id}', response_model=bool)
async def delete_operation_type(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await OperationTypeService.delete(type_id, enterprise_id)
