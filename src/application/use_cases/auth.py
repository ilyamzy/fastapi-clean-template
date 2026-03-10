import logging

from domain.entities import User
from domain.interfaces import IUnitOfWork
from domain.interfaces import IAuthService
from domain.dto import CheckTokenDTO


logger = logging.getLogger(__name__)


class AuthUseCases:
    
    def __init__(
        self,
        uow: IUnitOfWork,
        auth_service: IAuthService
    ):
        self.uow = uow
        self.auth_service = auth_service

    async def check_token(
        self,
        dto: CheckTokenDTO
    ) -> User:
        uid = self.auth_service.verify_token(dto.token)

        async with self.uow:
            user = await self.uow.users.get_by_id(id=uid)
            if not user:
                user=User(id=uid)
                await self.uow.users.add(user)
            await self.uow.commit()
        return user
