import datetime
import json

from influxdb_client import Point, WriteApi
from sqlalchemy import select

from src.core.db import get_influx_query
from src.core.config import InfluxSettings
from src.api.endpoints.mqtt.client import mqtt
from src.core.db import async_session_factory
from src.models.user import User
from src.models import TempScheduleEntry


def notify_device_target_flat_temperature(flat: int, temp: float):
    payload = f"0 {round(temp, 1)}"
    mqtt.client.publish(f"/mode/{flat}", payload, qos=1)


def notify_device_schedule_segment(flat: int, segment: TempScheduleEntry):
    # mode target_temp time(seconds)
    payload = f'2 {segment.target_temp} {max(segment.end_offset - (datetime.datetime.now() - segment.start_time).seconds, 1)}'
    mqtt.client.publish(f"/mode/{flat}", payload, qos=1)


def notify_device_disabled(flat: int):
    payload = f"3"
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

    if not data:
        return 6.66

    return data[0]["_value"]


async def toggle_flat(flat: int, state: bool):
    async with async_session_factory() as session:
        query = select(User).where(User.flat == flat)
        user = (await session.execute(query)).scalars().first()
        user.disabled = state
        await session.commit()


async def is_flat_disabled(flat: int):
    async with async_session_factory() as session:
        query = select(User).where(User.flat == flat)
        user = (await session.execute(query)).scalars().first()
        return user.disabled
