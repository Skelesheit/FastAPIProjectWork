from fastapi import APIRouter, Depends, Path, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import AssortmentTypeCreate, AssortmentTypeUpdate, AssortmentTypeOut
from src.services.resources.assortment_type_service import AssortmentTypeService

router = APIRouter(
    prefix="/assortment-types",
    tags=["assortment_type"]
)


@router.get('')
async def get_assortment_types(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        name: str | None = Query(default=None),
) -> list[AssortmentTypeOut]:
    return await AssortmentTypeService.list(enterprise_id, name=name)


@router.post('')
async def create_assortment_type(
        payload: AssortmentTypeCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> AssortmentTypeOut:
    return await AssortmentTypeService.create(payload, enterprise_id)


@router.get('/{type_id}')
async def get_assortment_type_by_id(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> AssortmentTypeOut:
    return await AssortmentTypeService.get(type_id, enterprise_id)


@router.put('/{type_id}')
async def update_assortment_type(
        payload: AssortmentTypeUpdate,
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> AssortmentTypeOut:
    return await AssortmentTypeService.update(type_id, payload, enterprise_id)


@router.delete('/{type_id}')
async def delete_assortment_type(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> bool:
    return await AssortmentTypeService.delete(type_id, enterprise_id)
