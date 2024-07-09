import uuid
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel
from app.mod.meta.model import BaseUUIDTimestampModel
from typing import List, Set

from ..role.model import RoleTable


class User(SQLModel):
    email: str = Field(unique=True)


class UserTable(User, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_users"

    keys: List["KeyTable"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "joined",
            "innerjoin": True,
            "cascade": "all, delete",
        },
    )


class Key(SQLModel):
    key: uuid.UUID = Field(
        default_factory=uuid.uuid4, nullable=False, index=True, unique=True
    )

    is_active: bool = Field(default=True)
    user_id: uuid.UUID = Field(
        sa_column=Column(
            ForeignKey("rbac_users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    role_id: uuid.UUID = Field(
        sa_column=Column(
            ForeignKey("rbac_roles.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )


class KeyTable(Key, BaseUUIDTimestampModel, table=True):
    __tablename__ = "rbac_keys"

    user: UserTable = Relationship(back_populates="keys")
    role: RoleTable = Relationship(
        back_populates="keys",
        sa_relationship_kwargs={"lazy": "joined", "innerjoin": True},
    )
