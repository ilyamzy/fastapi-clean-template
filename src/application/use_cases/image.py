import uuid

from domain.interfaces.image_storage import IImageStorage
from domain.entities.image import Image
from application.utils.image_processor import ImageProcessor


class ImageUseCases:
    def __init__(
        self,
        image_storage: IImageStorage
    ):
        self.image_storage = image_storage

    async def upload(self, raw_bytes: bytes) -> Image:
        image_id = str(uuid.uuid4())
        compressed_image = await ImageProcessor.process(
            image_id,
            raw_bytes
        )
        uploaded_image = await self.image_storage.put(compressed_image)
        return uploaded_image

    async def download(self, id: str) -> Image:
        return await self.image_storage.get(id)
