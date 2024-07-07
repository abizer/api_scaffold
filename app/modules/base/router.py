from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from app.core.config import settings
from app.utils.timer import timer

from .schema import InfoResponse
from .service import get_active_connections, get_active_transactions

router = APIRouter()


@router.get("/info")
async def info() -> InfoResponse:
    return InfoResponse(
        project_name=settings.PROJECT_NAME,
        mode=settings.MODE,
        build_info=settings.BUILD_INFO,
    )


@router.get("/db")
async def db_status() -> JSONResponse:
    if settings.DATABASE_ENGINE == "postgres":
        with timer() as t:
            n_active = await get_active_connections()
            t.lap()
            n_xact = await get_active_transactions()

        return {
            "status": "ok",
            "actives": n_active,
            "xacts": n_xact,
            # latencies look like "47.532ms ['45.287ms', '2.245ms']",
            # which is overall latency,
            # connection latency (because the first transaction needs to establish a connection)
            # and query latency (the second transaction reuses the connection from the first)
            "latencies": str(t),
            "name": settings.DATABASE_NAME,
            "engine": settings.DATABASE_ENGINE,
        }
    else:
        return {
            "status": "ok",
            "engine": settings.DATABASE_ENGINE,
        }
