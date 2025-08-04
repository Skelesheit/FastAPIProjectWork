from src.db.models import MachineType
from src.serializers.resources import MachineTypeCreate, MachineTypeUpdate, MachineTypeOut


class MachineTypeService:

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[MachineTypeOut]:
        objs = await MachineType.list_by_enterprise(enterprise_id, **kwargs)
        return [MachineTypeOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: MachineTypeCreate, enterprise_id: int) -> MachineTypeOut:
        obj = await MachineType.create_by_enterprise(enterprise_id, **data.model_dump())
        return MachineTypeOut.model_validate(obj)

    @classmethod
    async def get(cls, machine_type_id: int, enterprise_id: int) -> MachineTypeOut:
        obj = await MachineType.get_by_enterprise(machine_type_id, enterprise_id)
        return MachineTypeOut.model_validate(obj)

    @classmethod
    async def update(cls, machine_type_id: int, data: MachineTypeUpdate, enterprise_id: int) -> MachineTypeOut:
        obj = await MachineType.update_by_enterprise(
            id_=machine_type_id,
            enterprise_id=enterprise_id,
            **data.model_dump()
        )
        return MachineTypeOut.model_validate(obj)

    @classmethod
    async def delete(cls, machine_type_id: int, enterprise_id: int) -> bool:
        return await MachineType.delete_by_enterprise(machine_type_id, enterprise_id)
