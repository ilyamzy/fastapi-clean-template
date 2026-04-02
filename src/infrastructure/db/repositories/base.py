from typing import (
    TypeVar,
    Generic,
    Type,
    List,
    Optional,
    Any,
    Sequence
)

from sqlalchemy import select
from sqlalchemy.orm import Load
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.mappers import BaseMapper
from infrastructure.db.models import Base
from application.exceptions import ValueAlreadyExists
from domain.interfaces import IBaseRepository


ModelType = TypeVar("ModelType", bound=Base)
DomainType = TypeVar("DomainType")


class SqlAlchemyBaseRepository(
    IBaseRepository[DomainType],
    Generic[ModelType, DomainType]
):
    load_options: Sequence[Load] = []

    def __init__(
        self,
        session: AsyncSession,
        model_cls: ModelType,
        mapper: Type[BaseMapper]
    ):
        self.session = session
        self.model_cls = model_cls
        self.mapper = mapper

    async def _get_with_options(self, id: Any) -> Optional[ModelType]:
        stmt = (
            select(self.model_cls)
            .where(self.model_cls.id == id)
            .options(*self.load_options)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, domain_entity: DomainType) -> DomainType:
        try:
            model_instance = self.mapper.to_model(domain_entity)
            self.session.add(model_instance)
            await self.session.flush()
            result = await self._get_with_options(model_instance.id)
            return self.mapper.to_domain(result)
        except IntegrityError:
            await self.session.rollback()
            raise ValueAlreadyExists

    async def list(self) -> List[DomainType]:
        query = select(self.model_cls).options(*self.load_options)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.to_domain(m) for m in models]

    async def get_by_id(self, id: Any) -> Optional[DomainType]:
        model_instance = await self._get_with_options(id)
        if model_instance is None:
            return None
        return self.mapper.to_domain(model_instance)

    async def update(self, domain_entity: DomainType) -> Optional[DomainType]:
        try:
            model_instance = await self._get_with_options(domain_entity.id)
            if not model_instance:
                return None
            
            self.mapper.update_model(model_instance, domain_entity)
            await self.session.flush()
            return self.mapper.to_domain(model_instance)
        except IntegrityError:
            await self.session.rollback()
            raise ValueAlreadyExists

    async def delete(self, id: Any) -> bool:
        model_instance = await self._get_with_options(id)
        if not model_instance:
            return False
        await self.session.delete(model_instance)
        await self.session.flush()
        return True
    
    async def get_by_fields(
        self,
        **filters
    ) -> Optional[DomainType]:
        query = (
            select(self.model_cls)
            .filter_by(**filters)
            .options(*self.load_options)
        )
        result = await self.session.execute(query)
        model = result.unique().scalar_one_or_none()
        if model is None:
            return None
        return self.mapper.to_domain(model)

    async def list_by_fields(
        self,
        **filters
    ) -> list[DomainType]:
        query = (
            select(self.model_cls)
            .filter_by(**filters)
            .options(*self.load_options)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.to_domain(m) for m in models]
