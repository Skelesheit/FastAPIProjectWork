from fastapi import APIRouter, Depends, Query

from src.auth.dep import get_enterprise_by_user_id
from src.serializers.resources import ToolCreate, ToolUpdate, ToolOut
from src.services.resources.tool_service import ToolService

router = APIRouter(
    prefix="/tools",
    tags=["tools"]
)


@router.get('', response_model=list[ToolOut])
async def list_tools(
    enterprise_id: int = Depends(get_enterprise_by_user_id),
    name: str | None = Query(None),
):
    return await ToolService.list(enterprise_id=enterprise_id, name=name)


@router.post('', response_model=ToolOut)
async def create_tool(
    payload: ToolCreate,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolService.create(enterprise_id=enterprise_id, **payload.model_dump())


@router.get('/{tool_id}', response_model=ToolOut)
async def get_tool_by_id(
    tool_id: int,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolService.get(tool_id, enterprise_id)


@router.put('/{tool_id}', response_model=ToolOut)
async def update_tool(
    tool_id: int,
    payload: ToolUpdate,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolService.update(tool_id, enterprise_id, **payload.model_dump())


@router.delete('/{tool_id}')
async def delete_tool(
    tool_id: int,
    enterprise_id: int = Depends(get_enterprise_by_user_id),
):
    return await ToolService.delete(tool_id, enterprise_id)
