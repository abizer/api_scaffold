from uuid import UUID

from sqlalchemy import Column
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

class NamedEntity(SQLModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: Optional[str] = Field(nullable=True)
    resource_id: UUID = Field(foreign_key="rbac_resources.resource_id", nullable=False, unique=True)

class Organization(NamedEntity):
    pass
    
class OrganizationTable(Organization, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_orgs"

    resource: ResourceTable = Relationship(back_populates="organizations")
    projects: List["ProjectTable"] = Relationship(back_populates="organization")

class Project(NamedEntity):
    organization_id: UUID = Field(foreign_key="rbac_orgs.id")
    
class ProjectTable(Project, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_projects"

    resource: ResourceTable = Relationship(back_populates="projects")
    organization: OrganizationTable = Relationship(back_populates="projects")
    documents: List["DocumentTable"] = Relationship(back_populates="project")

class Document(NamedEntity):
    project_id: UUID = Field(foreign_key="rbac_projects.id")
    data: dict = Field(sa_column=Column(JSONB), default=lambda: {})
    
class DocumentTable(Document, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_docs"
    
    project: ProjectTable = Relationship(back_populates="documents")
    resource: ResourceTable = Relationship(back_populates="documents")

    

