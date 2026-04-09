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
from infrastructure.image_storage import (
    S3Storage,
    CachedStorage
)
from application.use_cases import (
    AuthUseCases,
    ImageUseCases
)
from application.exceptions import (
    InvalidToken
)
from domain.dto import (
    CheckTokenDTO
)
from domain.interfaces import (
    IUnitOfWork,
    IAuthService,
    IImageStorage
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

async def get_s3_client() -> AsyncGenerator:
    async with session.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION
    ) as client:
        yield client

async def get_image_storage(
    s3_client = Depends(get_s3_client)
) -> IImageStorage:
    return S3Storage(
        s3_client=s3_client,
        bucket=settings.S3_BUCKET,
        base_url=settings.BASE_URL
    )

async def get_cached_image_storage(
    base_storage: IImageStorage = Depends(get_image_storage)
) -> IImageStorage:
    return CachedStorage(
        base_storage=base_storage,
        cache_dir=settings.CACHE_DIR
    )

async def get_image_use_cases(
    storage: IImageStorage = Depends(get_cached_image_storage)
) -> ImageUseCases:
    return ImageUseCases(
        image_storage=storage
    )
