from fastapi import Depends, APIRouter, HTTPException
from influxdb_client import QueryApi, WriteApi
from itertools import chain

from src.core.db import get_influx_query, get_influx_write
from src.schemas.influx import SensorData
from src.api.endpoints.auth.core import current_user
from src.api.endpoints.flats.core import (
    notify_device_target_flat_temperature,
    save_target_flat_temperature,
)

router = APIRouter(prefix="/flats")


@router.post("/{flat}/target")
async def set_target_temperature(
    flat: int,
    temp: float,
    user: current_user(),  # type: ignore
    write_api: WriteApi = Depends(get_influx_write),
):
    save_target_flat_temperature(flat, temp, write_api=write_api)
    notify_device_target_flat_temperature(flat, temp)


@router.get("/{flat}/{measurement}", response_model=list[SensorData[float]])
async def get_measurement_data(
    flat: int,
    measurement: str,
    start: str,
    stop: str,
    window: str,
    tz: str,
    user: current_user(),  # type: ignore
    query_api: QueryApi = Depends(get_influx_query),
):
    match measurement:
        case "temp" | "humd" | "curr":
            pass
        case _:
            raise HTTPException(
                status_code=400, detail=f"bad measurement {measurement}"
            )

    query = f"""from(bucket: "default")\
    |> range(start: {start}, stop: {stop})\
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")\
    |> filter(fn: (r) => r["flat"] == "{flat}")\
    |> filter(fn: (r) => r["_field"] == "value")\
    |> aggregateWindow(every: {window}, fn: mean)"""

    tables = query_api.query(query)

    mapper = SensorData[float].from_flux_record(tz)

    return map(
        mapper,
        filter(
            lambda x: x.get_value() is not None,
            chain.from_iterable(table.records for table in tables),
        ),
    )
