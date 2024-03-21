from fastapi_mqtt import FastMQTT, MQTTConfig

from src.core.config import MQTTSettings


mqtt_cfg = MQTTConfig(
    host=MQTTSettings.host,
    password=MQTTSettings.password,
    username=MQTTSettings.username,
)

mqtt = FastMQTT(mqtt_cfg, client_id=MQTTSettings.client_id)
