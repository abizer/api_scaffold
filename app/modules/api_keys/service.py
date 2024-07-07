import uuid6
from app.modules import crud
from .schema import ApiKeyCreate
from .model import ApiKey


async def create_api_key(api_key: ApiKeyCreate) -> ApiKey:
    return await crud.api_key.create(obj_in=api_key)


async def get_api_keys() -> list[ApiKey]:
    return await crud.api_key.get_multi()


async def delete_api_key(api_key_id: uuid6.UUID) -> None:
    return await crud.api_key.remove(id=api_key_id)
