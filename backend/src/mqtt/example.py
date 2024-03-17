from fastapi import APIRouter
from src.auth.routes import current_user
from src.mqtt import get_last_val, mqtt_publish

mqtt_example_router = APIRouter(prefix="/mqtt")


@mqtt_example_router.get("/")
async def get_last_val_ep(
    user: current_user(),  # type: ignore
) -> str:
    return get_last_val()


@mqtt_example_router.post("/")
async def set_delay(delay: int):
    mqtt_publish("/act/delay/0", str(delay))
