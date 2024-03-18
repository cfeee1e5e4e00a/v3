from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from src.auth.routes import router as auth_router
from src.api.routers import example_router, log_router
from src.auth.core import get_user, create_user
from src.mqtt import init_mqtt
from src.mqtt.example import mqtt_example_router
from src.schemas.user import Role


async def create_user_if_not_exists(name: str, password: str, roles: list[Role]):
    user = await get_user(name)
    if user is None:
        print(f"Creating user {name}")
        await create_user(name, password, roles)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_user_if_not_exists("admin", "123", [Role.ADMIN])
    await create_user_if_not_exists("ilya", "qwe", [])
    await init_mqtt()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(log_router)
app.include_router(auth_router)
app.include_router(example_router)
app.include_router(mqtt_example_router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="NTI-API docs")
