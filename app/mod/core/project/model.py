from app.mod.meta.model import BaseUUIDTimestampModel
from sqlmodel import Field, Relationship
from uuid6 import UUID

from ..org.model import OrganizationTable

from ..role.model import ResourceTable

class Project(BaseUUIDTimestampModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)

    resource_id: UUID = Field(foreign_key="core_resources.id")
    organization_id: UUID = Field(foreign_key="core_organizations.id")
    
class ProjectTable(Project, table=True):
    __tablename__ = "core_projects"

    resource: ResourceTable = Relationship(back_populates="projects")
    organization: OrganizationTable = Relationship(back_populates="projects")
    
