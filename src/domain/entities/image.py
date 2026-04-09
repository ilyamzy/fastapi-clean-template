from pydantic import BaseModel


class Image(BaseModel):
    id: str
    url: str | None = None
    content: bytes
    mime_type: str
