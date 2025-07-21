import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.db.models import materials
from src.db.utils import consts


async def bind_materials_and_gost():
    async with get_session() as session:
        result = await session.execute(select(materials.Material))
        material_map = {m.name: m.id for m in result.scalars()}
        result = await session.execute(select(materials.GOST))
        gost_map = {g.number: g.id for g in result.scalars()}
        for key, list_value in consts.materials.items():
            session.add_all([
                materials.GOSTMaterial(gost_id=gost_id, material_id=material_map[key])
                for gost_id in [
                    gost_map[value]
                    for value in list_value
                ]])

        await session.commit()


async def insert_data():
    async with get_session() as session:
        for dict_key, dict_value in consts.operations.items():
            session.add_all([
                materials.Operation(operation_type=dict_key, name=value)
                for value in dict_value.values()])

        session.add_all([materials.Machine(name=dict_value)
                         for dict_key, dict_value in
                         consts.machines.items()])

        for dict_key, dict_value in consts.metals.items():
            session.add_all([materials.Metal(metal_type=dict_key, name=value) for value in dict_value])

        gosts = set()
        _materials = set()
        for keys, values in consts.materials.items():
            gosts.update(values)
            _materials.add(keys)
        session.add_all([materials.Material(name=item) for item in _materials])
        session.add_all([materials.GOST(number=item) for item in gosts])

        # наконец все родительские таблицы комитим
        await session.commit()

    await bind_materials_and_gost()

if __name__ == '__main__':
    asyncio.run(insert_data())