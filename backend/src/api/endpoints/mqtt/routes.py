from fastapi import APIRouter

from ..auth.routes import current_user
from .core import mqtt

router = APIRouter(prefix="/mqtt")


@router.get("/")
async def get_last_value(
    user: current_user(),  # type: ignore
) -> str:
    # TODO: get last value from Influx
    return 0


@router.post("/{delay}")
async def set_delay(delay: int):
    mqtt.client.publish("/act/delay/0", str(delay))
    return f"{delay=} отправлено в '/act/led/0'"
