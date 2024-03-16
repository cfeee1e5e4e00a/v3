from fastapi import APIRouter, Depends, HTTPException, Cookie
from backend.backend.auth import get_current_user
from typing import Annotated
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.backend.db import get_db_session

router = APIRouter(
    prefix="/example",
    tags=["example"]
)

@router.get("/")
async def example(
        access_token: Annotated[str | None, Cookie()] = None,
        session: AsyncSession = Depends(get_db_session)
):
    user = get_current_user(access_token)

    pass
