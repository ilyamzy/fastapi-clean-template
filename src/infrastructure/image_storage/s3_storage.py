import io
import os
from typing import Any

from botocore.exceptions import ClientError

from domain.interfaces import IImageStorage
from domain.entities import Image
from application.exceptions import ImageNotFoundException


class S3Storage(IImageStorage):
    def __init__(
        self,
        s3_client: Any,
        bucket: str,
        base_url: str
    ):
        self.s3_client = s3_client
        self.bucket = bucket
        self.base_url = base_url

    async def put(self, image: Image) -> Image:
        key = f'images/{image.id}'
        fp = io.BytesIO(image.content)

        async with self.s3_client as client:
            await client.upload_fileobj(
                fp,
                self.bucket,
                key,
                ExtraArgs={"ContentType": image.mime_type}
            )
        
        image.url = f'{self.base_url}/{key}'
        return image

    async def get(self, id: str) -> Image:
        key = f'images/{id}'
        fp = io.BytesIO()
        try:
            async with self.s3_client as client:
                await client.download_fileobj(
                    self.bucket,
                    key,
                    fp
                )
        except ClientError as e:
            if e.response['Error']['Code'] in ["404", "NoSuchKey"]:
                raise ImageNotFoundException(id)
            raise e
        fp.seek(0)
        content = fp.read()
        name, ext = os.path.splitext(id)
        ext = ext.lstrip(".").lower()

        return Image(
            id=name,
            content=content,
            format=ext,
            mime_type=f'image/{ext}'
        )
