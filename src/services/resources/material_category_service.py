from src.db.models import MaterialCategory
from src.serializers.resources import MaterialCategoryCreate, MaterialCategoryUpdate, MaterialCategoryOut
from src.services.errors import NotFound


# категория материала
class MaterialCategoryService:

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[MaterialCategoryOut]:
        objs = await MaterialCategory.list_by_enterprise(enterprise_id, **kwargs)
        return [MaterialCategoryOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: MaterialCategoryCreate, enterprise_id: int) -> MaterialCategoryOut:
        obj =  await MaterialCategory.create_by_enterprise(enterprise_id, **data.model_dump())
        return MaterialCategoryOut.model_validate(obj)

    @classmethod
    async def get(cls, category_id: int, enterprise_id: int) -> MaterialCategoryOut:
        obj = await MaterialCategory.get_by_enterprise(category_id, enterprise_id)
        if obj is None:
            raise NotFound()
        return MaterialCategoryOut.model_validate(obj)

    @classmethod
    async def update(cls, category_id: int, data: MaterialCategoryUpdate, enterprise_id: int) -> MaterialCategoryOut:
        obj = await MaterialCategory.update_by_enterprise(
            id_=category_id,
            enterprise_id=enterprise_id,
            **data.model_dump()
        )
        return MaterialCategoryOut.model_validate(obj)

    @classmethod
    async def delete(cls, category_id: int, enterprise_id: int) -> bool:
        return await MaterialCategory.delete_by_enterprise(category_id, enterprise_id)
