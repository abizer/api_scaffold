from typing import Generic, List, Optional, Type, TypeVar
import uuid

from fastapi import HTTPException


from .model import OrganizationTable, ProjectTable, DocumentTable, NamedEntity
from app.mod.meta.crud import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select
from sqlalchemy.orm import aliased

from ..user.model import KeyTable
from ..role.model import ResourceTable, RoleResourceTable, RoleTable

ModelType = TypeVar("ModelType", bound=NamedEntity)


class NamedEntityCreate(NamedEntity):
    pass


class NamedEntityUpdate(NamedEntity):
    pass


class NamedEntityCRUD(
    CRUDBase[ModelType, NamedEntityCreate, NamedEntityUpdate], Generic[ModelType]
):
    def __init__(self, model: Type[ModelType], name: str):
        # ie what type of namedentity are we, ie org, project, document, etc
        self.name = name
        super().__init__(model)

    async def get_all(self) -> List[ModelType]:
        db_session = self.db.session
        query = select(self.model)
        return (await db_session.exec(query)).scalars().all()

    async def get_by_name(
        self, name: str, db_session: AsyncSession | None = None
    ) -> Optional[ModelType]:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.name == name)
        return (await db_session.exec(query)).one_or_none()

    async def get_for_key(
        self, key: uuid.UUID, db_session: AsyncSession | None = None
    ) -> List[ModelType]:
        db_session = db_session or self.db.session

        RoleResource = aliased(RoleResourceTable)
        Key = aliased(KeyTable)

        subquery = (
            select(RoleResource.resource_id)
            .join(Key, RoleResource.role_id == Key.role_id)
            .where(Key.key == key)
            .subquery()
        )

        query = select(self.model).where(self.model.resource_id.in_(subquery))
        return (await db_session.exec(query)).scalars().all()

    async def create_from_parent(
        self, name: str, parent: NamedEntity, db_session: AsyncSession | None = None
    ) -> ModelType:
        db_session = db_session or self.db.session

        create = NamedEntityCreate(name=name, resource_id=parent.resource_id)
        return await self.create(obj_in=create, db_session=db_session)


class CRUDOrg(NamedEntityCRUD[OrganizationTable]):
    async def create_from_name(
        self,
        name: str,
        role_id: uuid.UUID | None = None,
        db_session: AsyncSession | None = None,
    ) -> tuple[ModelType, uuid.UUID]:
        db_session = db_session or self.db.session

        # need to wrap this whole thing in a transaction
        async with db_session.begin_nested() as t:
            # first, create the resource
            # naming convention will be <entity_type>:<name>
            resource = ResourceTable(name=f"{self.name}:{name}")
            db_session.add(resource)
            await db_session.flush()

            if not role_id:
                # if we've not been given a role, generate one for this resource
                # naming convention for now will be role:<org>.<proj>.<doc>
                role = RoleTable(name=f"role:{name}")
                db_session.add(role)
                await db_session.flush()
                role_id = role.role_id

            # now, associate the role with the resource
            role_resource = RoleResourceTable(
                role_id=role_id, resource_id=resource.resource_id
            )
            db_session.add(role_resource)
            await db_session.flush()

            # finally, create the entity
            entity = self.model(name=name, resource_id=resource.resource_id)
            db_session.add(entity)
            await db_session.flush()

            try:
                await t.commit()
            except exc.IntegrityError as e:
                await t.rollback()
                # TODO(abizer): throw something better than HTTPException
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to create resource {self.name}:{name}",
                ) from e

        return entity, role_id


org = CRUDOrg(OrganizationTable, "org")


class CRUDProject(NamedEntityCRUD[ProjectTable]):
    pass


project = CRUDProject(ProjectTable, "project")


class CRUDDocument(NamedEntityCRUD[DocumentTable]):
    pass


document = CRUDDocument(DocumentTable, "document")
