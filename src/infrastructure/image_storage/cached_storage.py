import logging

from diskcache import Cache

from domain.interfaces import IImageStorage
from domain.entities import Image


logger = logging.getLogger(__name__)


class CachedStorage(IImageStorage):
    def __init__(self, base_storage: IImageStorage, cache_dir: str):
        self.base_storage = base_storage
        self.cache = Cache(directory=cache_dir)

    async def put(self, image: Image) -> Image:
        self.cache[image.id] = image
        result = await self.base_storage.put(image)
        self.cache[image.id] = result
        return result

    async def get(self, id: str) -> Image:
        if id in self.cache:
            logger.info(f"File {id} in cache!")
            return self.cache[id]

        logger.info(f"File {id} not in cache! Loading from S3")
        image = await self.base_storage.get(id)
        self.cache[id] = image
        return image
