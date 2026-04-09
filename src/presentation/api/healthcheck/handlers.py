import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from presentation.dependencies import engine


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"]
)


@router.get("")
async def health():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=503
        )
