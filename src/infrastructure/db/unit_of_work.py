from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from infrastructure.db.repositories.user import SqlAlchemyUserRepository
from domain.interfaces.unit_of_work import IUnitOfWork


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None
        self._users: SqlAlchemyUserRepository | None = None

    async def __aenter__(self):
        self._session = self.session_factory()
        self._users = SqlAlchemyUserRepository(self._session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    @property
    def users(self) -> SqlAlchemyUserRepository:
        return self._users
