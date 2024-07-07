from pydantic import BaseModel
from .model import ApiKeyBase

from app.utils.partial import optional


@optional()
class ApiKeyCreate(ApiKeyBase):
    pass


@optional()
class ApiKeyUpdate(ApiKeyBase):
    pass
