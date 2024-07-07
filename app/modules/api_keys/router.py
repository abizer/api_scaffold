from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import uuid6

from app.modules.api_keys.model import ApiKey
from app.modules.api_keys.schema import ApiKeyCreate
from .service import create_api_key, delete_api_key, get_api_keys

from app.core.auth import AuthBearer, get_current_user

router = APIRouter()

# check that these routes are authenticated
@router.post("", dependencies=[Depends(AuthBearer())], response_model=ApiKey)
async def create(user = Depends(get_current_user)) -> ApiKey:
    return await create_api_key(ApiKeyCreate())


@router.get("", response_model=list[ApiKey])
async def list() -> list[ApiKey]:
    return await get_api_keys()


@router.delete("/{api_key_id}", dependencies=[Depends(AuthBearer())])
async def delete(api_key_id: str, user = Depends(get_current_user)) -> JSONResponse:
    deleted = await delete_api_key(api_key_id)
    return JSONResponse(
        status_code=200, content={"message": f"Api key {deleted.api_key} deleted"}
    )
