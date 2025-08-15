from typing import List

from fastapi import APIRouter, Depends, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import MaterialCreate, MaterialUpdate, MaterialOut
from src.services.resources.material_service import MaterialService

router = APIRouter(
    prefix="/materials",
    tags=["materials"]
)


@router.get('')
async def list_materials(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        brand: str | None = Query(None),
) -> list[MaterialOut]:
    return await MaterialService.list(enterprise_id=enterprise_id, brand=brand)


@router.post('')
async def create_material(
        payload: MaterialCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
) -> MaterialOut:
    return await MaterialService.create(enterprise_id=enterprise_id, **payload.model_dump())


@router.get('/{material_id}')
async def get_material_by_id(
        material_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
) -> MaterialOut:
    return await MaterialService.get(material_id, enterprise_id)


@router.put('/{material_id}')
async def update_material(
        material_id: int,
        payload: MaterialUpdate,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
) -> MaterialOut:
    return await MaterialService.update(material_id, enterprise_id, **payload.model_dump())


@router.delete('/{material_id}')
async def delete_material(
        material_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await MaterialService.delete(material_id, enterprise_id)
