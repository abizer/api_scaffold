from fastapi import APIRouter

from .meta.router import meta

v1_router = APIRouter()
v1_router.include_router(meta, prefix="/meta", tags=["meta"])
