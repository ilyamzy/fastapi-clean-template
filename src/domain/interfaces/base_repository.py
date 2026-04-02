from abc import ABC, abstractmethod
from typing import (
    Optional,
    TypeVar,
    Generic,
    List,
    Any
)


T = TypeVar("T")


class IBaseRepository(Generic[T], ABC):

    @abstractmethod
    def add(self, T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        self,
        domain_entity: T
    ) -> Optional[T]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(
        self,
        id: Any
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def list_by_fields(
        self,
        **filters
    ) -> List[T]:
        raise NotImplementedError
