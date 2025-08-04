from fastapi import APIRouter, Depends

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import (
    AssortmentCreate,
    AssortmentUpdate,
    AssortmentOut
)
from src.services.resources.assortment_service import AssortmentService

router = APIRouter(prefix="/assortments", tags=["Assortments"])


@router.get("/", response_model=list[AssortmentOut])
async def list_assortments(
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await AssortmentService.list(enterprise_id)


@router.get("/{assortment_id}", response_model=AssortmentOut)
async def get_assortment(
        assortment_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await AssortmentService.get(assortment_id, enterprise_id)


@router.post("/", response_model=AssortmentOut)
async def create_assortment(
        data: AssortmentCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await AssortmentService.create(enterprise_id, data)


@router.put("/{assortment_id}", response_model=AssortmentOut)
async def update_assortment(
        assortment_id: int,
        data: AssortmentUpdate,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await AssortmentService.update(assortment_id, enterprise_id, data)


@router.delete("/{assortment_id}", response_model=bool)
async def delete_assortment(
        assortment_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await AssortmentService.delete(assortment_id, enterprise_id)
