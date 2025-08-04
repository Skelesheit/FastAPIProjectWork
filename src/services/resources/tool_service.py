# src/services/resources/tool_service.py

from typing import Any
from sqlalchemy.orm import selectinload, Load

from src.db.models import Tool
from src.serializers.resources import ToolOut, ToolCreate, ToolUpdate


class ToolService:

    @classmethod
    def get_options(cls) -> list[Load]:
        return [selectinload(Tool.machine)]

    @classmethod
    async def get(cls, id_: int, enterprise_id: int, **kwargs: Any) -> ToolOut:
        obj = await Tool.get_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return ToolOut.model_validate(obj)

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs: Any) -> list[ToolOut]:
        objs = await Tool.list_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return [ToolOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, enterprise_id: int, **kwargs: Any) -> ToolOut:
        obj = await Tool.create_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        print("created tool with machine: ", obj.machine.name)
        return ToolOut.model_validate(obj)

    @classmethod
    async def update(cls, id_: int, enterprise_id: int, **kwargs: Any) -> ToolOut:
        obj = await Tool.update_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return ToolOut.model_validate(obj)

    @classmethod
    async def delete(cls, id_: int, enterprise_id: int) -> bool:
        return await Tool.delete_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id
        )
