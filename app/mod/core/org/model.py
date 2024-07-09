from uuid6 import UUID
from app.mod.meta.model import BaseUUIDTimestampModel
from sqlmodel import Field, Relationship
from typing import List

from ..role.model import ResourceTable

class Organization(BaseUUIDTimestampModel):
    name: str = Field(nullable=False, index=True, unique=True)
    description: str = Field(nullable=True)
    resource_id: UUID = Field(foreign_key="core_resources.id")
    
class OrganizationTable(Organization, table=True):
    __tablename__ = "core_organizations"

    resource: ResourceTable = Relationship(back_populates="organizations")
    projects: List["ProjectTable"] = Relationship(back_populates="organization")
