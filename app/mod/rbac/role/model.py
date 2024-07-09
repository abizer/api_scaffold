import uuid
from app.mod.meta.model import BaseUUIDModel, BaseUUIDTimestampModel, TimestampMixin
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

class RoleResourceTable(BaseUUIDModel, table=True):
    __tablename__ = "rbac_role_resource_associations"

    role_id: uuid.UUID = Field(foreign_key="rbac_roles.id", index=True)
    resource_id: uuid.UUID = Field(foreign_key="rbac_resources.resource_id", index=True)

class ResourceTable(SQLModel, table=True):
    __tablename__ = "rbac_resources"

    # keep a name for convenience
    name: str = Field(nullable=False, index=True, unique=True)
    resource_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    roles: List["RoleTable"] = Relationship(back_populates="resources", link_model=RoleResourceTable)
    
    organizations: List["OrganizationTable"] = Relationship(back_populates="resource")
    projects: List["ProjectTable"] = Relationship(back_populates="resource")
    documents: List["DocumentTable"] = Relationship(back_populates="resource")

class Role(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=True)

    has_read: bool = Field(default=False)
    has_write: bool = Field(default=False)
    has_delete: bool = Field(default=False)

class RoleTable(Role, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_roles"

    keys: List["KeyTable"] = Relationship(back_populates="role", sa_relationship_kwargs={"cascade": "all, delete"})
    resources: List[ResourceTable] = Relationship(back_populates="roles", link_model=RoleResourceTable)
    




