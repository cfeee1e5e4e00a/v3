from fastapi import Depends, APIRouter

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.log_entry import LogEntry
from src.core.db import get_db_session


router = APIRouter(prefix="/log", tags=["log", "logs"])


@router.get("/")
async def root(session: AsyncSession = Depends(get_db_session)):
    query = select(LogEntry)
    res = await session.execute(query)
    entries = res.scalars().all()

    return {"message": "Hello World", "entries": list(map(lambda a: a.note, entries))}


@router.post("/")
async def some_post(text: str, session: AsyncSession = Depends(get_db_session)):
    query = insert(LogEntry).values(note=text)
    await session.execute(query)
    await session.commit()
