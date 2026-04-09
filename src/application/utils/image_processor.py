import io
import asyncio
from typing import Tuple

from PIL import Image as PIL_Image, ImageOps

from domain.entities.image import Image

PILLOW_FORMAT_TO_MIME = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
    "GIF": "image/gif",
    "BMP": "image/bmp",
    "TIFF": "image/tiff",
}

class ImageProcessor:
    TARGET_MAX_BYTES = 400 * 1024
    MAX_SIZE = (1920, 1920)
    MIN_QUALITY = 40
    START_QUALITY = 85
    STEP = 5

    @classmethod
    def _sync_process(cls, data: bytes) -> Tuple[bytes, str, str]:
        with io.BytesIO(data) as in_io:
            with PIL_Image.open(in_io) as img:
                original_mime = PILLOW_FORMAT_TO_MIME.get(img.format, "image/jpeg")
                
                img = ImageOps.exif_transpose(img)

                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")

                img.thumbnail(cls.MAX_SIZE, PIL_Image.LANCZOS)

                quality = cls.START_QUALITY
                best_bytes = None

                while quality >= cls.MIN_QUALITY:
                    out_io = io.BytesIO()
                    img.save(
                        out_io,
                        format="WEBP",
                        quality=quality,
                        method=6,
                        lossless=False
                    )
                    current_bytes = out_io.getvalue()
                    best_bytes = current_bytes

                    if len(current_bytes) <= cls.TARGET_MAX_BYTES:
                        break

                    quality -= cls.STEP

                return best_bytes, "webp", original_mime

    @classmethod
    async def process(cls, image_id: str, data: bytes) -> Image:
        processed_bytes, ext, original_mime = await asyncio.to_thread(
            cls._sync_process,
            data
        )

        if len(processed_bytes) >= len(data):
            return Image(
                id=image_id,
                content=data,
                format="original",
                mime_type=original_mime
            )

        return Image(
            id=image_id,
            content=processed_bytes,
            format=ext,
            mime_type="image/webp"
        )
