from src.db.models import Gost
from src.serializers.resources import GostCreate, GostUpdate, GostOut


# категория материала
class GostService:

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[GostOut]:
        objs = await Gost.list_by_enterprise(enterprise_id, **kwargs)
        return [GostOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: GostCreate, enterprise_id: int) -> GostOut:
        obj = await Gost.create_by_enterprise(enterprise_id, **data.model_dump())
        return GostOut.model_validate(obj)

    @classmethod
    async def get(cls, gost_id: int, enterprise_id: int) -> GostOut:
        obj = await Gost.get_by_enterprise(gost_id, enterprise_id)
        return GostOut.model_validate(obj)

    @classmethod
    async def update(cls, gost_id: int, data: GostUpdate, enterprise_id: int) -> GostOut:
        obj = await Gost.update_by_enterprise(
            id_=gost_id,
            enterprise_id=enterprise_id,
            **data.model_dump()
        )
        return GostOut.model_validate(obj)

    @classmethod
    async def delete(cls, gost_id: int, enterprise_id: int) -> bool:
        return await Gost.delete_by_enterprise(gost_id, enterprise_id)
