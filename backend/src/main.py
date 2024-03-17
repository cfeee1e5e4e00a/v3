from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.routes import router as auth_router
from src.api.routers import example_router, log_router
from src.core.db import init_db
from src.auth.core import get_user, create_user
from src.schemas.user import User, RoleEnum


async def create_user_if_not_exists(name: str, password: str, roles: list[RoleEnum]):
    user = await get_user(name)
    if user is None:
        print(f'Creating user {name}')
        await create_user(name, password, roles)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await create_user_if_not_exists('admin', '123', [RoleEnum.ADMIN])
    await create_user_if_not_exists('ilya', 'qwe', [])
    yield
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(log_router)
app.include_router(auth_router)
app.include_router(example_router)
