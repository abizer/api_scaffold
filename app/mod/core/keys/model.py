import uuid
from sqlmodel import Field, Relationship
from uuid6 import UUID

from app.mod.meta.model import BaseUUIDTimestampModel


class Key(BaseUUIDTimestampModel):
    key: uuid.UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )

    user_id: UUID = Field(foreign_key="core_users.id")
    role_id: UUID = Field(foreign_key="core_roles.id")
    is_active: bool = Field(default=True)


class KeyTable(Key, table=True):
    __tablename__ = "core_keys"

    user: "UserTable" = Relationship(back_populates="keys")
    role: "RoleTable" = Relationship(back_populates="keys")