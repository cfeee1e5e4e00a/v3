import asyncio

from gmqtt import Client as MQTTClient

from src.api.endpoints.flats.temperature import get_schedule_entries, get_current_segment
from src.api.endpoints.mqtt.client import mqtt
from src.api.endpoints.flats.core import (
    get_latest_flat_temperature,
    is_flat_disabled,
    notify_device_disabled,
    notify_device_target_flat_temperature, notify_device_schedule_segment,
)
from src.core.config import MQTTSettings
from src.core.logger import logger


@mqtt.on_disconnect()
def reconnect(client: MQTTClient, packet, exc=None):
    logger.info("MQTT disconnected, reconnecting...")
    asyncio.get_running_loop().run_until_complete(client.connect(MQTTSettings.host))


@mqtt.subscribe("/startup/#")
async def on_device_startup(
    client: MQTTClient, topic: str, payload: str, qos: int, properties
):
    flat = topic.split("/")[2]

    # check if flat is disabled
    is_disabled = await is_flat_disabled(flat)
    if is_disabled:
        notify_device_disabled(flat)
        return

    # check if flat has time schedule
    if (segment := await get_current_segment(int(flat))) is not None:
        notify_device_schedule_segment(int(flat), segment)
        return


    # not disabled, no schedule
    temp = get_latest_flat_temperature(flat)
    notify_device_target_flat_temperature(flat, temp)
