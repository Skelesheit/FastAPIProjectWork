from fastapi import APIRouter

from src.handlers.resources.materials import router as materials_router
from src.handlers.resources.assortment_type import router as assortment_type_router
from src.handlers.resources.material_categories import router as material_categories_router
from src.handlers.resources.gosts import router as gosts_router

"""
from src.handlers.resources.machines import router as machines_router
from src.handlers.resources.toolings import router as toolings_router
from src.handlers.resources.tools import router as tools_router
from src.handlers.resources.assortment_gost import router as assortment_gost_router
from src.handlers.resources.operation_type import router as operation_type_router
from src.handlers.resources.methods import router as methods_router
from src.handlers.resources.machine_type import router as machine_type_router
"""

router = APIRouter()

# всё только, для того чтобы взаимодействовать с материалом
router.include_router(materials_router)
router.include_router(material_categories_router)
router.include_router(gosts_router)
router.include_router(assortment_type_router)

"""
router.include_router(machines_router)
router.include_router(toolings_router)
router.include_router(tools_router)
router.include_router(material_categories_router)

router.include_router(assortment_type_router)
router.include_router(assortment_gost_router)
router.include_router(operation_type_router)
router.include_router(methods_router)
router.include_router(machine_type_router)
"""
