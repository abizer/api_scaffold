import uuid
from sqlalchemy import exc, select, insert
from typing import Optional
from app.core.db.middleware import AsyncSession

from ...meta.crud import CRUDBase
from .model import User, UserTable, Key, KeyTable


class UserCreate(User):
    pass


class UserUpdate(User):
    pass


class KeyCreate(Key):
    pass


class KeyUpdate(Key):
    pass


class CRUDKey(CRUDBase[KeyTable, KeyCreate, KeyUpdate]):
    async def get_for_user(
        self, user_id: uuid.UUID, db_session: AsyncSession | None = None
    ) -> Optional[KeyTable]:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.user_id == user_id)
        return (await db_session.exec(query)).scalars().all()

    async def get_all(self):
        db_session = self.db.session
        query = select(self.model)
        return (await db_session.exec(query)).scalars().all()


class CRUDUser(CRUDBase[UserTable, UserCreate, UserUpdate]):
    async def get_by_email(
        self, email: str, db_session: AsyncSession | None = None
    ) -> Optional[UserTable]:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.email == email)
        result = await db_session.exec(query)
        return result.unique().scalars().one_or_none()

    async def get_all(self):
        db_session = self.db.session
        query = select(self.model)
        return (await db_session.exec(query)).scalars().all()

    async def create_from_email(
        self, email: str, db_session: AsyncSession | None = None
    ) -> UserTable:
        db_session = db_session or self.db.session

        user = UserCreate(email=email)
        db_user = UserTable.model_validate(user)
        db_session.add(db_user)
        try:
            await db_session.commit()
        except exc.IntegrityError as e:
            await db_session.rollback()
            raise e

        # this can fail too
        await db_session.refresh(db_user)
        return db_user


key = CRUDKey(KeyTable)
user = CRUDUser(UserTable)
