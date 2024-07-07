from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import ModeEnum, settings

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

connect_args = {"check_same_thread": False}


def get_engine_for_db_type(db_type: str) -> Engine:
    match db_type:
        case "postgres":
            return postgres_engine
        case "sqlite":
            return sqlite_engine
        case _:
            raise ValueError(f"Invalid database engine: {db_type}")


def get_uri_for_db_type(db_type: str) -> str:
    match db_type:
        case "postgres":
            return str(settings.ASYNC_POSTGRES_URI)
        case "sqlite":
            return str(settings.ASYNC_SQLITE_URI)
        case _:
            raise ValueError(f"Invalid database engine: {db_type}")


postgres_engine = create_async_engine(
    url=str(settings.ASYNC_POSTGRES_URI),
    echo=False,
    poolclass=NullPool if settings.MODE == ModeEnum.TEST else AsyncAdaptedQueuePool,
)

postgres_sessionmaker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

sqlite_engine = create_async_engine(
    url=str(settings.ASYNC_SQLITE_URI),
    echo=False,
    poolclass=NullPool if settings.MODE == ModeEnum.TEST else AsyncAdaptedQueuePool,
    connect_args=connect_args,
)

sqlite_sessionmaker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sqlite_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# engine_celery = create_async_engine(
#     str(settings.ASYNC_CELERY_BEAT_DATABASE_URI),
#     echo=False,
#     poolclass=NullPool
#     if settings.MODE == ModeEnum.TEST
#     else AsyncAdaptedQueuePool,  # Asincio pytest works with NullPool
#     # pool_size=POOL_SIZE,
#     # max_overflow=64,
# )

# SessionLocalCelery = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine_celery,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )
