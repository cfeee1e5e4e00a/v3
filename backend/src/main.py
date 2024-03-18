from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from src.api import routers, mqtt, get_user, create_user
from src.models.user import Role


async def create_user_if_not_exists(name: str, password: str, roles: list[Role]):
    user = await get_user(name)
    if user is None:
        print(f"Creating user {name}")
        await create_user(name, password, roles)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mqtt.mqtt_startup()
    await create_user_if_not_exists("admin", "123", [Role.ADMIN])
    await create_user_if_not_exists("ilya", "qwe", [])
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
