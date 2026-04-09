import logging
import io

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    HTTPException,
)
from fastapi.responses import StreamingResponse

from presentation.api.image.serializers import (
    UploadImageResponse
)
from presentation.dependencies import (
    get_current_user,
    get_image_use_cases
)
from application.use_cases import ImageUseCases
from application.exceptions import ImageNotFoundException
from domain.entities import User


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


# @router.post(
#     "",
#     status_code=201,
#     response_model=UploadImageResponse
# )
# async def upload_image(
#     file: UploadFile,
#     user: User = Depends(get_current_user),
#     use_cases: ImageUseCases = Depends(get_image_use_cases)
# ):
#     try:
#         raw_bytes = await file.read()
#         image = await use_cases.upload(raw_bytes)
#         response_data = UploadImageResponse(
#             url=image.url
#         )
#         return response_data
#     except Exception as e:
#         logger.exception(e)
#         raise HTTPException(status_code=500)


@router.get(
    "/{filename}",
    status_code=200
)
async def download_image(
    filename: str,
    user: User = Depends(get_current_user),
    use_cases: ImageUseCases = Depends(get_image_use_cases)
):
    try:
        image = await use_cases.download(filename)
        return StreamingResponse(
            io.BytesIO(image.content),
            media_type=image.mime_type
        )
    except ImageNotFoundException:
        raise HTTPException(status_code=404)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500)
