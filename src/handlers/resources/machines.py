from typing import List

from fastapi import APIRouter, Depends, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import MachineCreate, MachineUpdate, MachineOut
from src.services.resources.machine_service import MachineService

router = APIRouter(
    prefix="/machines",
    tags=["machines"]
)


@router.get('', response_model=List[MachineOut])
async def list_machines(
    enterprise_id: int = Depends(get_enterprise_by_user_id),
    name: str | None = Query(None),
):
    return await MachineService.list(enterprise_id=enterprise_id, name=name)


@router.post('', response_model=MachineOut)
async def create_machine(
    payload: MachineCreate,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await MachineService.create(enterprise_id=enterprise_id, **payload.model_dump())


@router.get('/{machine_id}', response_model=MachineOut)
async def get_machine_by_id(
    machine_id: int,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await MachineService.get(machine_id, enterprise_id)


@router.put('/{machine_id}', response_model=MachineOut)
async def update_machine(
    machine_id: int,
    payload: MachineUpdate,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await MachineService.update(machine_id, enterprise_id, **payload.model_dump())


@router.delete('/{machine_id}')
async def delete_machine(
    machine_id: int,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await MachineService.delete(machine_id, enterprise_id)
