from abc import ABC, abstractmethod

from domain.entities import Image


class IImageStorage(ABC):

    @abstractmethod
    async def put(
        self,
        image: Image
    ) -> Image:
        raise NotImplementedError
    
    @abstractmethod
    async def get(
        self,
        filename: str
    ) -> Image:
        raise NotImplementedError
