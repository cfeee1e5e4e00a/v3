from typing import Annotated

from fastapi import Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import get_current_user
from src.core.db import get_db_session


from ..routers import example_router


@example_router.get("/")
async def example(
    access_token: Annotated[str | None, Cookie()] = None,
    session: AsyncSession = Depends(get_db_session),
):
    user = get_current_user(access_token)

    pass
