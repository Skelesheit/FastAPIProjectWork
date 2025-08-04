from src.db.models import MaterialCategory
from src.serializers.resources import MaterialCategoryCreate, MaterialCategoryUpdate, MaterialCategoryOut


# категория материала
class MaterialCategoryService:

    @classmethod
    async def list(cls, enterprise_id: int, **kwargs) -> list[MaterialCategoryOut]:
        objs = await MaterialCategory.list_by_enterprise(enterprise_id, **kwargs)
        return [MaterialCategoryOut.model_validate(obj) for obj in objs]

    @classmethod
    async def create(cls, data: MaterialCategoryCreate, enterprise_id: int) -> MaterialCategory:
        return await MaterialCategory.create_by_enterprise(enterprise_id, **data.model_dump())

    @classmethod
    async def get(cls, category_id: int, enterprise_id: int) -> MaterialCategoryOut:
        obj = await MaterialCategory.get_by_enterprise(category_id, enterprise_id)
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
    async def delete(cls, category_id: int, enterprise_id: int) -> None:
        obj = await MaterialCategory.delete_by_enterprise(category_id, enterprise_id)
