from backend.db import get_db_session
from backend.model import LogEntry
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth import router as auth_router
from example.router import router as example_router
from conf import LOGIN_CALLBACK_URI

app = FastAPI()

origins = [
    LOGIN_CALLBACK_URI
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "PUT", "GET", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

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


app.include_router(auth_router)
app.include_router(example_router)
