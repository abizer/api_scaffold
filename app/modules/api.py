from fastapi import APIRouter

from .base.router import router as base_router
from .api_keys.router import router as api_keys_router

v1_router = APIRouter()
v1_router.include_router(base_router, prefix="/base", tags=["base"])
v1_router.include_router(api_keys_router, prefix="/api-keys", tags=["api-keys"])
