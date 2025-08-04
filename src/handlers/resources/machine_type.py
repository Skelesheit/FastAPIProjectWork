from typing import List

from fastapi import APIRouter, Depends, Path, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import MachineTypeCreate, MachineTypeUpdate, MachineTypeOut
from src.services.resources.machine_type_service import MachineTypeService

router = APIRouter(
    prefix="/machine-types",
    tags=["machine_type"]
)


@router.get('', response_model=List[MachineTypeOut])
async def get_machine_types(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        name: str | None = Query(default=None),
):
    return await MachineTypeService.list(enterprise_id, name=name)


@router.post('', response_model=MachineTypeOut)
async def create_machine_type(
        payload: MachineTypeCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MachineTypeService.create(payload, enterprise_id)


@router.get('/{type_id}', response_model=MachineTypeOut)
async def get_machine_type_by_id(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MachineTypeService.get(type_id, enterprise_id)


@router.put('/{type_id}', response_model=MachineTypeOut)
async def update_machine_type(
        payload: MachineTypeUpdate,
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MachineTypeService.update(type_id, payload, enterprise_id)


@router.delete('/{type_id}', response_model=bool)
async def delete_machine_type(
        type_id: int = Path(...),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    return await MachineTypeService.delete(type_id, enterprise_id)
