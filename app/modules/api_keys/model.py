import uuid
from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr
from sqlmodel import Field

from app.modules.base.model import BaseUUIDTimestampModel


class ApiKeyBase(BaseUUIDTimestampModel):
    api_key: uuid.UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )


class ApiKey(ApiKeyBase, table=True):
    __tablename__ = "api_keys"
