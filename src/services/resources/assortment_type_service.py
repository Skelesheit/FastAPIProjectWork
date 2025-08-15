from typing import List

from sqlalchemy.orm import selectinload, Load


from src.db.models import AssortmentType, Gost
from src.serializers.resources import AssortmentTypeCreate, AssortmentTypeUpdate, AssortmentTypeOut


class AssortmentTypeService:

    @classmethod
    def get_options(cls) -> list:
        return [selectinload(Gost)]

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[AssortmentTypeOut]:
        objs = await AssortmentType.list_by_enterprise(
            enterprise_id,
            options=cls.get_options(),
            **kwargs)
        return [AssortmentTypeOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: AssortmentTypeCreate, enterprise_id: int) -> AssortmentTypeOut:
        obj = await AssortmentType.create_by_enterprise(enterprise_id, **data.model_dump())
        return AssortmentTypeOut.model_validate(obj)

    @classmethod
    async def get(cls, type_id: int, enterprise_id: int) -> AssortmentTypeOut:
        obj = await AssortmentType.get_by_enterprise(
            type_id,
            enterprise_id,
            options = cls.get_options(),
        )
        return AssortmentTypeOut.model_validate(obj)

    @classmethod
    async def update(cls, type_id: int, data: AssortmentTypeUpdate, enterprise_id: int) -> AssortmentTypeOut:
        obj = await AssortmentType.update_by_enterprise(
            id_=type_id,
            enterprise_id=enterprise_id,
            **data.model_dump()
        )
        return AssortmentTypeOut.model_validate(obj)

    @classmethod
    async def delete(cls, type_id: int, enterprise_id: int) -> bool:
        return await AssortmentType.delete_by_enterprise(type_id, enterprise_id)
