from uuid import UUID

from uuid6 import uuid7
from datetime import UTC, datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field
from sqlmodel import SQLModel as _SQLModel


# id: implements proposal uuid7 draft4
class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampMixin:
    # use tz-aware UTC timestamps everywhere
    # so it's easy for postgres comparisons
    created_at: datetime = Field(
        nullable=True,
        default=func.utc_timestamp(),
        sa_type=DateTime(timezone=True),
    )

    updated_at: datetime = Field(
        nullable=True,
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": func.utc_timestamp()},
    )


class BaseIDModel(SQLModel):
    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )


class BaseUUIDModel(SQLModel):
    id: UUID | None = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class BaseIDTimestampModel(TimestampMixin, BaseIDModel):
    pass


class BaseUUIDTimestampModel(TimestampMixin, BaseUUIDModel):
    pass
