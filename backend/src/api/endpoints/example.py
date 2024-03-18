from typing import Annotated

from fastapi import Depends, Cookie, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

# from src.auth.routers import get_current_user
from src.core.db import get_db_session


router = APIRouter(prefix="/example", tags=["example"])


@router.get("/")
async def example(
    access_token: Annotated[str | None, Cookie()] = None,
    session: AsyncSession = Depends(get_db_session),
):
    # user = get_current_user(access_token)

    pass
