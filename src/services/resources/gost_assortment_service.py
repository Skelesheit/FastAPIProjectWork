from typing import Any

from sqlalchemy.orm import selectinload

from src.db.models import GostAssortment
from src.serializers.resources import (
    GostAssortmentCreate,
    GostAssortmentUpdate,
    GostAssortmentOut,
)


class GostAssortmentService:

    @property
    def options(self) -> list:
        return [
            selectinload(GostAssortment.gost),
            selectinload(GostAssortment.assortment_type),
        ]

    @classmethod
    async def get(cls, id_: int, enterprise_id: int, **kwargs: Any) -> GostAssortmentOut:
        obj = await GostAssortment.get_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.options,
        )
        return GostAssortmentOut.model_validate(obj)

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs: Any) -> list[GostAssortmentOut]:
        objs = await GostAssortment.list_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.options,
            **kwargs
        )
        return [GostAssortmentOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, enterprise_id: int, data: GostAssortmentCreate) -> GostAssortmentOut:
        obj = await GostAssortment.create_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.options,
            **data.model_dump()
        )
        return GostAssortmentOut.model_validate(obj)

    @classmethod
    async def update(cls, id_: int, enterprise_id: int, data: GostAssortmentUpdate) -> GostAssortmentOut:
        obj = await GostAssortment.update_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.options,
            **data.model_dump(exclude_unset=True)
        )
        return GostAssortmentOut.model_validate(obj)

    @classmethod
    async def delete(cls, id_: int, enterprise_id: int) -> bool:
        return await GostAssortment.delete_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id
        )
