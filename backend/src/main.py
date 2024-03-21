from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from src.models.user import Role
from src.api.endpoints.mqtt.client import mqtt
import src.api.endpoints.mqtt.core
from src.api import routers, get_user, create_user


async def create_admin_if_not_exists(name: str, password: str):
    user = await get_user(name)
    if user is None:
        print(f"Creating user {name}")
        await create_user(name, password, Role.ADMIN, 0)


async def create_user_if_not_exists(name: str, password: str, role: Role, flat):
    user = await get_user(name)
    if user is None:
        print(f"Creating user {name}")
        await create_user(name, password, role, flat)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mqtt.mqtt_startup()
    await create_admin_if_not_exists("admin", "123")
    await create_user_if_not_exists("user1", "123", Role.USER_FLOOR_2, 1)
    await create_user_if_not_exists("user2", "123", Role.USER_FLOOR_2, 2)
    await create_user_if_not_exists("user3", "123", Role.USER_FLOOR_2, 3)
    await create_user_if_not_exists("user4", "123", Role.USER_FLOOR_1, 4)
    await create_user_if_not_exists("user5", "123", Role.USER_FLOOR_1, 5)
    await create_user_if_not_exists("user6", "123", Role.USER_FLOOR_1, 6)
    yield
    await mqtt.mqtt_shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in routers:
    app.include_router(router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="NTI-API docs")
