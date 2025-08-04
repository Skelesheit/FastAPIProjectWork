from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import (
    GostAssortmentCreate,
    GostAssortmentUpdate,
    GostAssortmentOut
)
from src.services.resources.gost_assortment_service import GostAssortmentService

# надо ещё списки или batch проработать на CRUD

router = APIRouter(
    prefix="/gost-assortments",
    tags=["GostAssortments"]
)


@router.get("/", response_model=list[GostAssortmentOut])
async def list_gost_assortments(
        enterprise_id: Annotated[int, Depends(get_enterprise_by_user_id)],
):
    return await GostAssortmentService.list(enterprise_id)


@router.get("/{id}", response_model=GostAssortmentOut)
async def get_gost_assortment(
        id: int,
        enterprise_id: Annotated[int, Depends(get_enterprise_by_user_id)],
):
    return await GostAssortmentService.get(id, enterprise_id)


@router.post("/", response_model=GostAssortmentOut)
async def create_gost_assortment(
        data: GostAssortmentCreate,
        enterprise_id: Annotated[int, Depends(get_enterprise_by_user_id)],
):
    return await GostAssortmentService.create(enterprise_id, data)


@router.put("/{id}", response_model=GostAssortmentOut)
async def update_gost_assortment(
        id: int,
        data: GostAssortmentUpdate,
        enterprise_id: Annotated[int, Depends(get_enterprise_by_user_id)],
):
    return await GostAssortmentService.update(id, enterprise_id, data)


@router.delete("/{id}", response_model=bool)
async def delete_gost_assortment(
        id: int,
        enterprise_id: Annotated[int, Depends(get_enterprise_by_user_id)],
):
    return await GostAssortmentService.delete(id, enterprise_id)
