import asyncio

from gmqtt import Client as MQTTClient

from src.api.endpoints.mqtt.client import mqtt
from src.api.endpoints.flats.core import (
    get_latest_flat_temperature,
    notify_device_target_flat_temperature,
)
from src.core.config import MQTTSettings
from src.core.logger import logger


@mqtt.on_disconnect()
def reconnect(client: MQTTClient, packet, exc=None):
    logger.info("MQTT disconnected, reconnecting...")
    asyncio.get_running_loop().run_until_complete(client.connect(MQTTSettings.host))


@mqtt.subscribe("/startup/#")
def on_device_startup(
    client: MQTTClient, topic: str, payload: str, qos: int, properties
):
    flat = topic.split("/")[2]
    temp = get_latest_flat_temperature(flat)
    notify_device_target_flat_temperature(flat, temp)
