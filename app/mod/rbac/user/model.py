import uuid
from sqlmodel import Field, Relationship, SQLModel
from app.mod.meta.model import BaseUUIDTimestampModel
from typing import List, Set

from ..role.model import RoleTable

class User(BaseUUIDTimestampModel):
    email: str = Field(unique=True)
    
class UserTable(User, table=True):
    __tablename__ = "rbac_users"

    keys: List["KeyTable"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})

class Key(BaseUUIDTimestampModel):
    key: uuid.UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )

    is_active: bool = Field(default=True)
    user_id: uuid.UUID = Field(foreign_key="rbac_users.id")
    role_id: uuid.UUID = Field(foreign_key="rbac_roles.id")


class KeyTable(Key, table=True):
    __tablename__ = "rbac_keys"

    user: UserTable = Relationship(back_populates="keys")
    role: RoleTable = Relationship(back_populates="keys", sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})