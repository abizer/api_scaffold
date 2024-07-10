from uuid import UUID

from uuid import UUID
from datetime import UTC, datetime
import uuid

from sqlalchemy import DateTime, func, Column, UUID as SA_UUID
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
        default=func.now(),
        sa_type=DateTime(timezone=True),
    )

    updated_at: datetime = Field(
        nullable=True,
        sa_type=DateTime(timezone=True),
        default=func.now(),
        sa_column_kwargs={"onupdate": func.now()},
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
        primary_key=True,
        default_factory=uuid.uuid4,
        nullable=False,
    )


class BaseIDTimestampModel(TimestampMixin, BaseIDModel):
    pass


class BaseUUIDTimestampModel(TimestampMixin, BaseUUIDModel):
    pass
