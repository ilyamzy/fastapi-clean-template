from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    url: str
