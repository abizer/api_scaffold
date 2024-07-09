import uuid
from sqlmodel import Field, Relationship
from uuid6 import UUID

from app.mod.meta.model import BaseUUIDTimestampModel


class ApiKeyBase(BaseUUIDTimestampModel):
    api_key: uuid.UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )


class ApiKey(ApiKeyBase, table=True):
    __tablename__ = "api_keys"

class ApiKeyUserAssociationsBase(BaseUUIDTimestampModel):
    user_id: UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )    
    api_key_id: UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )
    

class ApiKeyUserAssociations(ApiKeyUserAssociationsBase, table=True):
    __tablename__ = "api_key_user_associations"

    user = Relationship(back_populates="api_keys")
    api_key = Relationship(back_populates="users")
    

class ApiKeyRoleAssociationsBase(BaseUUIDTimestampModel):
    api_key_id: UUID = Field(foreign_key="api_keys.id")
    role_id: UUID = Field(foreign_key="roles.id")

class ApiKeyRoleAssociations(ApiKeyRoleAssociationsBase, table=True):
    __tablename__ = "api_key_role_associations"

    api_key = Relationship(back_populates="roles")
    role = Relationship(back_populates="api_keys")