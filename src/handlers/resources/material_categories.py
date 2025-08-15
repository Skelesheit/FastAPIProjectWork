from fastapi import APIRouter, Depends, Path, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import (
    MaterialCategoryCreate,
    MaterialCategoryUpdate,
    MaterialCategoryOut
)
from src.services.resources.material_category_service import MaterialCategoryService

router = APIRouter(
    prefix='/material-categories',
    tags=['Material Categories']
)


@router.get('')
async def get_material_categories(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        name: str | None = Query(default=None),
) -> list[MaterialCategoryOut]:
    return await MaterialCategoryService.list(enterprise_id, name=name)


@router.post('')
async def create_material_category(
        payload: MaterialCategoryCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> MaterialCategoryOut:
    return await MaterialCategoryService.create(payload, enterprise_id)


@router.get('/{category_id}')
async def get_material_category_by_id(
        category_id: int = Path(..., gt=0),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> MaterialCategoryOut:
    return await MaterialCategoryService.get(category_id, enterprise_id)


@router.put("/{category_id}")
async def update_material_category(
        category_id: int,
        payload: MaterialCategoryUpdate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> MaterialCategoryOut:
    return await MaterialCategoryService.update(category_id, payload, enterprise_id)


@router.delete("/{category_id}")
async def delete_material_category(
        category_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
) -> bool:
    return await MaterialCategoryService.delete(category_id, enterprise_id)
