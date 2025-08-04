from fastapi import APIRouter, Depends, HTTPException, Path, status, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import (
    MaterialCategoryCreate,
    MaterialCategoryUpdate,
    MaterialCategoryOut
)
from src.services.resources.material_category_service import MaterialCategoryService

router = APIRouter(
    prefix='/material-categories',
    tags=['Material Categories']
)


@router.get('', response_model=list[MaterialCategoryOut])
async def get_material_categories(
        enterprise_id: int = Depends(get_enterprise_by_user_id),
        name: str | None = Query(default=None),
):
    try:
        return await MaterialCategoryService.list(enterprise_id, name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('', response_model=MaterialCategoryOut)
async def create_material_category(
        payload: MaterialCategoryCreate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    try:
        return await MaterialCategoryService.create(payload, enterprise_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{category_id}', response_model=MaterialCategoryOut)
async def get_material_category_by_id(
        category_id: int = Path(..., gt=0),
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    try:
        obj = await MaterialCategoryService.get(category_id, enterprise_id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{category_id}", response_model=MaterialCategoryOut)
async def update_material_category(
        category_id: int,
        payload: MaterialCategoryUpdate,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    try:
        return await MaterialCategoryService.update(category_id, payload, enterprise_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material_category(
        category_id: int,
        enterprise_id: int = Depends(get_enterprise_by_user_id)
):
    try:
        await MaterialCategoryService.delete(category_id, enterprise_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
