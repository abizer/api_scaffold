from sqlmodel import Field, Relationship, SQLModel
from uuid6 import UUID
from app.mod.meta.model import BaseUUIDTimestampModel
from typing import List

class User(BaseUUIDTimestampModel):
    email: str = Field(nullable=False, index=True, unique=True)
    
class UserTable(User, table=True):
    __tablename__ = "core_users"

    keys: List["KeyTable"] = Relationship(back_populates="user")
    roles: List["RoleTable"] = Relationship(back_populates="users", link_model="UserRolesTable")

class UserRolesTable(SQLModel, table=True):
    __tablename__ = "core_user_role_associations"

    user_id: UUID = Field(foreign_key="core_users.id")
    role_id: UUID = Field(foreign_key="core_roles.id")