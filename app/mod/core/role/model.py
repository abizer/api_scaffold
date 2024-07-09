import uuid6
from app.mod.meta.model import BaseUUIDTimestampModel, TimestampMixin
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from uuid6 import UUID

class Role(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=True)

    has_read: bool = Field(default=False)
    has_write: bool = Field(default=False)
    has_delete: bool = Field(default=False)

class RoleTable(Role, BaseUUIDTimestampModel, table=True):
    __tablename__ = "core_roles"

    keys: List["KeyTable"] = Relationship(back_populates="role")
    users: List["UserTable"] = Relationship(back_populates="roles", link_model="UserRolesTable")

class Resource(SQLModel):
    # eventually we'll make this a hierarchical address
    resource_id: UUID = Field(default_factory=uuid6.uuid4(), primary_key=True)
    resource_type: str
    

class ResourceTable(Resource, TimestampMixin, table=True):
    __tablename__ = "core_resources"

    roles: Relationship(back_populates="resources", link_model="RoleResourceTable")
    resources: Relationship(back_populates="roles", link_model="RoleResourceTable")


class RoleResourceTable(SQLModel, table=True):
    __tablename__ = "core_role_resource_associations"

    role_id: UUID = Field(foreign_key="core_roles.id", index=True)
    resource_id: UUID = Field(foreign_key="core_resources.id", index=True)