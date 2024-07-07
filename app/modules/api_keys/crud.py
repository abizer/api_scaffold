from app.modules.base.crud import CRUDBase
from .model import ApiKey

from .schema import ApiKeyCreate, ApiKeyUpdate


class CRUDApiKey(CRUDBase[ApiKey, ApiKeyCreate, ApiKeyUpdate]):
    pass


api_key = CRUDApiKey(ApiKey)
