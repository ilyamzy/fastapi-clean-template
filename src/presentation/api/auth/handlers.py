import logging

from fastapi import APIRouter, Depends, HTTPException

from presentation.dependencies import (
    get_current_user
)
from application.exceptions.token import InvalidToken
from domain.entities.user import User


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post("")
async def authenticate(
    user: User = Depends(get_current_user)
):
    try:
        return {"user_id": user.id}
    except InvalidToken:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500)
