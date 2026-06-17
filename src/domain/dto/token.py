from pydantic import BaseModel


class CheckTokenDTO(BaseModel):
    token: str
