from src.db.models import Method
from src.serializers.resources import MethodCreate, MethodUpdate, MethodOut


class MethodService:

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[MethodOut]:
        objs = await Method.list_by_enterprise(enterprise_id, **kwargs)
        print(objs)
        return [MethodOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: MethodCreate, enterprise_id: int) -> MethodOut:
        obj = await Method.create_by_enterprise(enterprise_id, **data.model_dump())
        return MethodOut.model_validate(obj)

    @classmethod
    async def get(cls, method_id: int, enterprise_id: int) -> MethodOut:
        obj = await Method.get_by_enterprise(method_id, enterprise_id)
        print(obj)
        return MethodOut.model_validate(obj)

    @classmethod
    async def update(cls, method_id: int, data: MethodUpdate, enterprise_id: int) -> MethodOut:
        obj = await Method.update_by_enterprise(
            id_=method_id,
            enterprise_id=enterprise_id,
            **data.model_dump()
        )
        return MethodOut.model_validate(obj)

    @classmethod
    async def delete(cls, method_id: int, enterprise_id: int) -> bool:
        return await Method.delete_by_enterprise(method_id, enterprise_id)
