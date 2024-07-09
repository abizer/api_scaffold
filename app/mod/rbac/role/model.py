import uuid
from app.mod.meta.model import BaseUUIDModel, BaseUUIDTimestampModel, TimestampMixin
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

class RoleResourceTable(BaseUUIDModel, table=True):
    __tablename__ = "rbac_role_resource_associations"

    role_id: uuid.UUID = Field(foreign_key="rbac_roles.id", index=True)
    resource_id: uuid.UUID = Field(foreign_key="rbac_resources.resource_id", index=True)

    role: "RoleTable" = Relationship(back_populates="resource")
    resource: "ResourceTable" = Relationship(back_populates="role")

class ResourceTable(SQLModel, table=True):
    __tablename__ = "rbac_resources"

    # keep a name for convenience
    name: str = Field(nullable=False, index=True, unique=True)
    resource_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    roles: List["RoleTable"] = Relationship(back_populates="resources", link_model=RoleResourceTable)
    
    organization: "OrganizationTable" = Relationship(back_populates="resources")
    project: "ProjectTable" = Relationship(back_populates="resources")
    document: "DocumentTable" = Relationship(back_populates="resources")

class Role(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=True)

    has_read: bool = Field(default=False)
    has_write: bool = Field(default=False)
    has_delete: bool = Field(default=False)

class RoleTable(Role, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_roles"

    keys: List["KeyTable"] = Relationship(back_populates="role")
    resources: List["ResourceTable"] = Relationship(back_populates="role", link_model=RoleResourceTable)
    




