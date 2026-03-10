from pydantic import (
    BaseModel,
    ConfigDict
)


class User(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True
    )

    id: str | None = None
