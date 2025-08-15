from typing import Any

from sqlalchemy.orm import selectinload

from src.db.models import Material, AssortmentType
from src.serializers.resources import (
    MaterialOut
)


class MaterialService:

    @classmethod
    def get_options(cls) -> list:
        return [
            selectinload(Material.category),
            selectinload(Material.assortment_type)
            .selectinload(AssortmentType.gost)
        ]

    @classmethod
    async def get(cls, id_: int, enterprise_id: int, **kwargs: Any) -> MaterialOut:
        obj = await Material.get_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return MaterialOut.model_validate(obj)

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs: Any) -> list[MaterialOut]:
        objs = await Material.list_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return [MaterialOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, enterprise_id: int, **kwargs: Any) -> MaterialOut:
        obj = await Material.create_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        print("test obj: ", obj.category.name)
        return MaterialOut.model_validate(obj)

    @classmethod
    async def update(cls, id_: int, enterprise_id: int, **kwargs: Any) -> MaterialOut:
        obj = await Material.update_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return MaterialOut.model_validate(obj)

    @classmethod
    async def delete(cls, id_: int, enterprise_id: int) -> bool:
        return await Material.delete_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id
        )
