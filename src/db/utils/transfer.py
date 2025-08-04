import asyncio

from sqlalchemy import select

from src.db import get_session
from src.db import models
from src.db.models import OperationType
from src.db.utils import consts


async def bind_materials_and_gost():
    async with get_session() as session:
        result = await session.execute(select(models.AssortmentType))
        material_map = {m.name: m.id for m in result.scalars()}
        result = await session.execute(select(models.Gost))
        gost_map = {g.number: g.id for g in result.scalars()}

        for key, list_value in consts.materials.items():
            session.add_all(
                [
                    models.GostAssortment(
                        gost_id=gost_id,
                        assortment_type_id=material_map[key],
                        is_general=True
                    )
                    for gost_id in [
                    gost_map[value]
                    for value in list_value
                ]
                ]
            )
        await session.commit()


async def insert_data():
    async with get_session() as session:
        for dict_key, dict_value in consts.operations.items():
            operation_type = OperationType(
                name=dict_key,
                is_general=True
            )
            session.add(operation_type)
            await session.flush()
            session.add_all(
                [
                    models.Method(
                        name=value,
                        operation_type_id=operation_type.id,
                        is_general=True
                    )
                    for value in dict_value.values()
                ]
            )
        await session.flush()

        result = await session.execute(select(models.Method).limit(1))
        first_method = result.scalar_one_or_none()

        session.add_all(
            [
                models.MachineType(
                    name=dict_value,
                    method_id=first_method.id,
                    is_general=True,
                )
                for dict_key, dict_value in
                consts.machines.items()
            ]
        )

        await session.flush()

        for dict_key, dict_value in consts.metals.items():
            session.add_all(
                [
                    models.MaterialCategory(
                        material_type=dict_key,
                        name=value,
                        is_general=True
                    )
                    for value in dict_value
                ]
            )

        await session.flush()

        gosts = set()
        materials = set()
        for keys, values in consts.materials.items():
            gosts.update(values)
            materials.add(keys)
        session.add_all(
            [
                models.AssortmentType(name=item, is_general=True)
                for item in materials
            ]
        )
        session.add_all(
            [
                models.Gost(number=item, is_general=True)
                for item in gosts
            ]
        )

        # наконец все родительские таблицы комитим
        await session.commit()

    await bind_materials_and_gost()


if __name__ == '__main__':
    asyncio.run(insert_data())
