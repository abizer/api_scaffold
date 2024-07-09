from copy import copy, deepcopy
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.mod.meta.model import BaseUUIDTimestampModel
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional, Set

from ..role.model import ResourceTable

# class ResourceEntity(SQLModel):
#     entity_type: str = Field(nullable=False)
#     name: str = Field(nullable=False)
#     description: str = Field(nullable=True)

#     resource_id: UUID = Field(foreign_key="rbac_resources.id")
#     parent_id: UUID = Field(foreign_key="rbac_entities.id", nullable=True)

#     data: dict = Field(sa_column=Column(JSONB))


# class ResourceEntityTable(ResourceEntity, BaseUUIDTimestampModel, table=True):
#     __tablename__ = "rbac_entities"

#     resource: ResourceTable = Relationship(back_populates="entities")
#     parent: "ResourceEntityTable" = Relationship(back_populates="children")
#     children: Set["ResourceEntityTable"] = Relationship(back_populates="parent")


# unfortunately we don't really use the NamedEntity as intended, just as a pydantic type
class NamedEntity(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: Optional[str] = Field(nullable=True)
    resource_id: UUID = Field(
        sa_column=Column(
            ForeignKey("rbac_resources.resource_id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )
    )


class Organization(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: Optional[str] = Field(nullable=True)
    resource_id: UUID = Field(
        sa_column=Column(
            ForeignKey("rbac_resources.resource_id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )
    )


class OrganizationTable(Organization, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_orgs"

    resource: ResourceTable = Relationship(
        back_populates="organizations",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    projects: List["ProjectTable"] = Relationship(
        back_populates="organization", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Project(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: Optional[str] = Field(nullable=True)
    resource_id: UUID = Field(
        sa_column=Column(
            # project resource_ids are not unique. Multiple projects in a single org will
            # share the same resource_id.
            ForeignKey("rbac_resources.resource_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    organization_id: UUID = Field(
        sa_column=Column(ForeignKey("rbac_orgs.id", ondelete="CASCADE"), nullable=False)
    )


class ProjectTable(Project, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_projects"

    resource: ResourceTable = Relationship(back_populates="projects")
    organization: OrganizationTable = Relationship(back_populates="projects")
    documents: List["DocumentTable"] = Relationship(
        back_populates="project", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Document(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: Optional[str] = Field(nullable=True)
    resource_id: UUID = Field(
        sa_column=Column(
            # document resource_ids are not unique. Multiple documents in a single project will
            # share the same resource_id.
            ForeignKey("rbac_resources.resource_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    project_id: UUID = Field(
        sa_column=Column(
            ForeignKey("rbac_projects.id", ondelete="CASCADE"), nullable=False
        )
    )
    data: dict = Field(sa_column=Column(JSONB), default=lambda: {})


class DocumentTable(Document, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_docs"

    project: ProjectTable = Relationship(back_populates="documents")
    resource: ResourceTable = Relationship(back_populates="documents")
