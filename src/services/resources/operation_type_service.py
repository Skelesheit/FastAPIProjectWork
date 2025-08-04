from src.db.models import OperationType
from src.serializers.resources import (
    OperationTypeCreate,
    OperationTypeUpdate,
    OperationTypeOut
)


class OperationTypeService:

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[OperationTypeOut]:
        objs = await OperationType.list_by_enterprise(enterprise_id, **kwargs)
        return [OperationTypeOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: OperationTypeCreate, enterprise_id: int) -> OperationTypeOut:
        obj = await OperationType.create_by_enterprise(enterprise_id, **data.model_dump())
        return OperationTypeOut.model_validate(obj)

    @classmethod
    async def get(cls, operation_type_id: int, enterprise_id: int) -> OperationTypeOut:
        obj = await OperationType.get_by_enterprise(operation_type_id, enterprise_id)
        return OperationTypeOut.model_validate(obj)

    @classmethod
    async def update(cls, operation_type_id: int, data: OperationTypeUpdate, enterprise_id: int) -> OperationTypeOut:
        obj = await OperationType.update_by_enterprise(
            id_=operation_type_id,
            enterprise_id=enterprise_id,
            **data.model_dump()
        )
        return OperationTypeOut.model_validate(obj)

    @classmethod
    async def delete(cls, operation_type_id: int, enterprise_id: int) -> bool:
        return await OperationType.delete_by_enterprise(operation_type_id, enterprise_id)
