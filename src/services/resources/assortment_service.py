from typing import Any
from sqlalchemy.orm import selectinload

from src.db.models import Assortment, GostAssortment
from src.serializers.resources import (
    AssortmentCreate,
    AssortmentUpdate,
    AssortmentOut
)


class AssortmentService:

    @classmethod
    def get_options(cls) -> list:
        return [
            selectinload(Assortment.gost_assortment_model)
                .selectinload(GostAssortment.gost),
            selectinload(Assortment.gost_assortment_model)
                .selectinload(GostAssortment.assortment_type),
        ]

    @classmethod
    async def get(cls, id_: int, enterprise_id: int) -> AssortmentOut:
        obj = await Assortment.get_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
        )
        return AssortmentOut.model_validate(obj)

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs: Any) -> list[AssortmentOut]:
        objs = await Assortment.list_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **kwargs
        )
        return [AssortmentOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, enterprise_id: int, data: AssortmentCreate) -> AssortmentOut:
        obj = await Assortment.create_by_enterprise(
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **data.model_dump()
        )
        print("gost assortment model: ", obj.gost_assortment_model)
        print("gost_assortment_model:", obj.gost_assortment_model)
        print("type:", type(obj.gost_assortment_model))

        return AssortmentOut.model_validate(obj)

    @classmethod
    async def update(cls, id_: int, enterprise_id: int, data: AssortmentUpdate) -> AssortmentOut:
        obj = await Assortment.update_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id,
            load_options=cls.get_options(),
            **data.model_dump(exclude_unset=True)
        )
        return AssortmentOut.model_validate(obj)

    @classmethod
    async def delete(cls, id_: int, enterprise_id: int) -> bool:
        return await Assortment.delete_by_enterprise(
            id_=id_,
            enterprise_id=enterprise_id
        )
