from fastapi import Depends, FastAPI
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db_session
from backend.model import LogEntry

app = FastAPI()


@app.get("/")
async def root(session: AsyncSession = Depends(get_db_session)):
    query = select(LogEntry)
    res = await session.execute(query)
    entries = res.scalars().all()

    return {"message": "Hello World", "entries": list(map(lambda a: a.note, entries))}


@app.post("/")
async def some_post(text: str, session: AsyncSession = Depends(get_db_session)):
    query = insert(LogEntry).values(note=text)
    await session.execute(query)
    await session.commit()
