from influxdb_client import Point, WriteApi
from src.core.config import InfluxSettings
from src.api import mqtt


def notify_device_target_flat_temperature(flat: int, temp: float):
    payload = f"0 {round(temp, 1)}"
    mqtt.client.publish(f"/mode/{flat}", payload, qos=1)


def save_target_flat_temperature(flat: int, temp: float, write_api: WriteApi):
    p = Point("target_temp").tag("flat", flat).field("value", temp)

    write_api.write(bucket="default", org=InfluxSettings.org, record=[p])
    write_api.close()
