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

from application.exceptions import ValueAlreadyExists
from infrastructure.db.mappers import BaseMapper
from infrastructure.db.models import Base


ModelType = TypeVar("ModelType", bound=Base)
DomainType = TypeVar("DomainType")


class SqlAlchemyBaseRepository(Generic[ModelType, DomainType]):
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
        result = await self.session.execute(select(self.model_cls))
        models = result.scalars().all()
        return [self.mapper.to_domain(m) for m in models]

    async def get_by_id(self, id: Any) -> Optional[DomainType]:
        model_instance = await self.session.get(self.model_cls, id)
        if model_instance:
            return self.mapper.to_domain(model_instance)
        return None

    async def update(self, id: Any, **payload) -> Optional[DomainType]:
        try:
            model_instance = await self.session.get(self.model_cls, id)
            if not model_instance:
                return None
            
            for key, value in payload.items():
                if hasattr(model_instance, key):
                    setattr(model_instance, key, value)
            
            await self.session.flush()
            result = await self._get_with_options(model_instance.id)
            return self.mapper.to_domain(result)
        except IntegrityError:
            await self.session.rollback()
            raise ValueAlreadyExists

    async def delete(self, id: Any) -> bool:
        model_instance = await self.session.get(self.model_cls, id)

        if not model_instance:
            return False
        await self.session.delete(model_instance)
        await self.session.flush()
        return True
    
    async def list_by_fields(
        self,
        **filters
    ) -> List[DomainType]:
        query = select(self.model_cls).filter_by(**filters)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.to_domain(m) for m in models]
