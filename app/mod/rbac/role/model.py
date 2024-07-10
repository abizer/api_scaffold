import uuid

from sqlalchemy import Column, ForeignKey
from app.mod.meta.model import BaseUUIDModel, BaseUUIDTimestampModel
from sqlmodel import Field, Relationship, SQLModel
from typing import List


class RoleResourceTable(BaseUUIDModel, table=True):
    __tablename__ = "rbac_role_resource_associations"

    role_id: uuid.UUID = Field(
        sa_column=Column(
            ForeignKey("rbac.rbac_roles.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    resource_id: uuid.UUID = Field(
        sa_column=Column(
            ForeignKey("rbac.rbac_resources.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )


class ResourceTable(SQLModel, table=True):
    __tablename__ = "rbac_resources"

    # the db column is created with default=uuid_generate_v4()
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # keep a name for convenience
    name: str = Field(nullable=False, index=True, unique=True)

    roles: List["RoleTable"] = Relationship(
        back_populates="resources", link_model=RoleResourceTable
    )

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

    keys: List["KeyTable"] = Relationship(
        back_populates="role", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    resources: List[ResourceTable] = Relationship(
        back_populates="roles", link_model=RoleResourceTable
    )
