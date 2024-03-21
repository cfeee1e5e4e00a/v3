import json

from influxdb_client import Point, WriteApi

from src.core.db import get_influx_query
from src.core.config import InfluxSettings
from src.api.endpoints.mqtt.client import mqtt


def notify_device_target_flat_temperature(flat: int, temp: float):
    payload = f"0 {round(temp, 1)}"
    mqtt.client.publish(f"/mode/{flat}", payload, qos=1)


def save_target_flat_temperature(flat: int, temp: float, write_api: WriteApi):
    p = Point("target_temp").tag("flat", flat).field("value", temp)

    write_api.write(bucket="default", org=InfluxSettings.org, record=[p])
    write_api.close()


def get_latest_flat_temperature(flat: int) -> float:
    query_api = next(get_influx_query())

    query = f"""from(bucket: "default")\
    |> range(start: -48h)
    |> filter(fn: (r) => r["_measurement"] == "target_temp")\
    |> filter(fn: (r) => r["flat"] == "{flat}")\
    |> filter(fn: (r) => r["_field"] == "value")\
    |> sort(columns: ["_time"], desc: true)\
    |> limit(n: 1)"""

    data = json.loads(query_api.query(query).to_json())

    return data[0]["_value"]
