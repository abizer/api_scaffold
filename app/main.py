from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.db.middleware import SQLModelMiddleware
from .core.db.session import engine
from .core.log import D, make_logger

from .modules.api import v1_router

logger = make_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    D("running in mode: %s", settings.MODE.value)
    D("%s startup complete", settings.PROJECT_NAME)
    yield
    # shutdown
    D("shutdown events complete")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.add_middleware(SQLModelMiddleware, custom_engine=engine)
app.add_middleware(
    CORSMiddleware,
    # eventually make these stricter
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/v1")


@app.get("/status")
def status() -> JSONResponse:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app)
