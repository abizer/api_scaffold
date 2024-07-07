from fastapi import APIRouter

from app.modules.api_keys.model import ApiKey
from app.modules.api_keys.schema import ApiKeyCreate
from .service import create_api_key, get_api_keys

router = APIRouter()


@router.post("", response_model=ApiKey)
async def create() -> ApiKey:
    return await create_api_key(ApiKeyCreate())


@router.get("", response_model=list[ApiKey])
async def list() -> list[ApiKey]:
    return await get_api_keys()
