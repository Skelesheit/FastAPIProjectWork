from typing import List

from fastapi import APIRouter, Depends, Path, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import AssortmentTypeCreate, AssortmentTypeUpdate, AssortmentTypeOut
from src.services.resources.assortment_type_service import AssortmentTypeService

router = APIRouter(
    prefix="/assortment-types",
    tags=["assortment_type"]
)


@router.get('', response_model=List[AssortmentTypeOut])
async def get_assortment_types(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        name: str | None = Query(default=None),
):
    return await AssortmentTypeService.list(enterprise_id, name=name)


@router.post('', response_model=AssortmentTypeOut)
async def create_assortment_type(
        payload: AssortmentTypeCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await AssortmentTypeService.create(payload, enterprise_id)


@router.get('/{type_id}', response_model=AssortmentTypeOut)
async def get_assortment_type_by_id(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await AssortmentTypeService.get(type_id, enterprise_id)


@router.put('/{type_id}', response_model=AssortmentTypeOut)
async def update_assortment_type(
        payload: AssortmentTypeUpdate,
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await AssortmentTypeService.update(type_id, payload, enterprise_id)


@router.delete('/{type_id}', response_model=bool)
async def delete_assortment_type(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await AssortmentTypeService.delete(type_id, enterprise_id)
