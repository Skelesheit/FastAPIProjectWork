from typing import Any
from sqlalchemy.orm import selectinload, Load

from src.db.models import Machine
from src.serializers.resources import MachineOut, MachineCreate, MachineUpdate


class MachineService:

    @classmethod
    def get_options(cls) -> list[Load]:
        return [selectinload(Machine.machine_type)]

    @classmethod
    async def get(cls, id_: int, enterprise_id: int, **kwargs: Any) -> MachineOut:
        obj = await Machine.get_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return MachineOut.model_validate(obj)

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs: Any) -> list[MachineOut]:
        objs = await Machine.list_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return [MachineOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, enterprise_id: int, **kwargs: Any) -> MachineOut:
        obj = await Machine.create_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        print("test obj: ", obj.machine_type.name)
        return MachineOut.model_validate(obj)

    @classmethod
    async def update(cls, id_: int, enterprise_id: int, **kwargs: Any) -> MachineOut:
        obj = await Machine.update_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return MachineOut.model_validate(obj)

    @classmethod
    async def delete(cls, id_: int, enterprise_id: int) -> bool:
        return await Machine.delete_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id
        )
