import aioboto3

from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from infrastructure.config import settings
from infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.services import (
    FirebaseAuthService
)
from application.use_cases import (
    AuthUseCases
)
from application.exceptions import (
    InvalidToken
)
from domain.dto import (
    CheckTokenDTO
)
from domain.interfaces import (
    IUnitOfWork,
    IAuthService
)


engine = create_async_engine(settings.DB_URL)
async_session_marker = async_sessionmaker(
    engine,
    expire_on_commit=False
)
auth_schema = HTTPBearer()
session = aioboto3.Session()


async def get_uow() -> AsyncGenerator[IUnitOfWork, None]:
    uow = SqlAlchemyUnitOfWork(async_session_marker)
    yield uow

def get_auth_service() -> IAuthService:
    return FirebaseAuthService()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_schema),
    uow: IUnitOfWork = Depends(get_uow),
    auth_service: IAuthService = Depends(get_auth_service)
):
    auth_use_cases = AuthUseCases(uow, auth_service)
    check_token_dto = CheckTokenDTO(token=token.credentials)
    try:
        return await auth_use_cases.check_token(check_token_dto)
    except InvalidToken:
        raise HTTPException(status_code=401)
