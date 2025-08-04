from typing import List

from fastapi import APIRouter, Path
from fastapi.params import Depends, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import GostCreate, GostUpdate, GostOut
from src.services.resources.gosts_service import GostService

router = APIRouter(
    prefix='/gosts',
    tags=['gosts']
)


@router.get('', response_model=List[GostOut])
async def get_gosts(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        number: str | None = Query(default=None),
):
    return await GostService.list(enterprise_id, number=number)


@router.post('', response_model=GostOut)
async def create_gost(
        payload: GostCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await GostService.create(payload, enterprise_id)


@router.get('/{gost_id}', response_model=GostOut)
async def get_gost_by_id(
        gost_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await GostService.get(gost_id, enterprise_id)


@router.put('/{gost_id}', response_model=GostOut)
async def update_gost(
        gost_id: int,
        payload: GostUpdate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await GostService.update(gost_id, payload, enterprise_id)


@router.delete('/{gost_id}', response_model=bool)
async def delete_gost(
        gost_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await GostService.delete(gost_id, enterprise_id)
