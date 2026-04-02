from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.repositories import SqlAlchemyBaseRepository
from infrastructure.db.mappers import UserMapper
from infrastructure.db.models import UserModel
from domain.interfaces import IUserRepository
from domain.entities import User


class SqlAlchemyUserRepository(
    IUserRepository,
    SqlAlchemyBaseRepository[UserModel, User]
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel, UserMapper)
