import asyncio
from typing import Any

from fastapi_mqtt import FastMQTT, MQTTConfig
from gmqtt import Client as MQTTClient

from src.core.config import MQTTSettings
from src.core.logger import logger

mqtt_cfg = MQTTConfig(
    host=MQTTSettings.host,
    password=MQTTSettings.password,
    username=MQTTSettings.username,
)
mqtt = FastMQTT(mqtt_cfg, client_id=MQTTSettings.client_id)


@mqtt.on_disconnect()
def reconnect(client: MQTTClient, packet, exc=None):
    logger.info("MQTT disconnected, reconnecting...")
    asyncio.get_running_loop().run_until_complete(client.connect(MQTTSettings.host))
