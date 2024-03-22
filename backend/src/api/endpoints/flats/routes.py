from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException
from influxdb_client import QueryApi, WriteApi
from itertools import chain

from sqlalchemy import delete, select

from src.api.endpoints.flats.temperature import remove_schedule
from src.core.db import get_influx_query, get_influx_write, async_session_factory
from src.models import TempScheduleEntry
from src.schemas.influx import SensorData
from src.api.endpoints.auth.core import current_user
from src.models.user import Role
from src.api.endpoints.flats.core import (
    get_latest_flat_temperature,
    notify_device_target_flat_temperature,
    notify_device_disabled,
    save_target_flat_temperature,
    toggle_flat,
)
from src.schemas.schedule import Schedule

router = APIRouter(prefix="/flats")


@router.post("/{flat}/toggle")
async def toggle_disable_flat(flat: int, state: str, user: current_user([Role.ADMIN])):  # type: ignore
    match state:
        case "true" | "false":
            pass
        case _:
            raise HTTPException(status_code=400, detail=f"bad state {state}")

    state = {'true': True, 'false': False}[state]

    await toggle_flat(flat, state)

    if state == False:
        await remove_schedule(flat)
        notify_device_disabled(flat)
    else:
        temp = get_latest_flat_temperature(flat)
        notify_device_target_flat_temperature(flat, temp)


@router.post("/{flat}/target")
async def set_target_temperature(
    flat: int,
    temp: float,
    user: current_user(),  # type: ignore
    write_api: WriteApi = Depends(get_influx_write),
):
    await remove_schedule(flat)
    save_target_flat_temperature(flat, temp, write_api=write_api)
    notify_device_target_flat_temperature(flat, temp)


@router.post("/{flat}/schedule")
async def set_flat_temp_schedule(
    flat: int,
    user: current_user(), # type: ignore
    schedule: Schedule,
):
    async with async_session_factory() as session:
        await session.execute(
            delete(TempScheduleEntry).where(TempScheduleEntry.flat == flat)
        )
        start_time = datetime.now()
        prev_offset = 0
        for entry in schedule.entries:
            session.add(
                TempScheduleEntry(
                    flat=flat,
                    start_time=start_time,
                    was_sent=False,
                    start_offset=prev_offset,
                    end_offset=entry.time,
                    target_temp=entry.temp,
                )
            )
            prev_offset = entry.time
        await session.commit()


@router.get("/{flat}/has_schedule")
async def flat_has_schedule(flat: int) -> bool:
    async with async_session_factory() as session:
        res = await session.execute(
            select(TempScheduleEntry).where(TempScheduleEntry.flat == flat)
        )
        return res.scalars().first() is not None


@router.post("/{flat}/can_decrease_energy")
async def check_flat_energy_possibility(
    flat: int,
    dDolya: float,
    query_api: QueryApi = Depends(get_influx_query),
) -> bool:
    last_taget_temp_query = f"""from(bucket: "default")
    |> range(start: -3d, stop: -0s)
    |> filter(fn: (r) => r["_measurement"] == "target_temp")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["flat"] == "{flat}")
    |> drop(columns: ["_measurement", "_field", "_time", "flat"])
    |> last()"""
    last_current_consumption_query = f"""from(bucket: "default")
    |> range(start: -3d, stop: -0s)
    |> filter(fn: (r) => r["_measurement"] == "consumption")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["flat"] == "{flat}")
    |> drop(columns: ["_measurement", "_field", "_time", "flat"])
    |> last()"""
    # TODO: parse queries to floats
    # TODO: count min_consumption from target_temp
    # TODO: current_consumption - min_consumption = dCumsuction
    # TODO: if dCumsuction > dDolya then true else false


@router.post("/flats/can_decrease_energy")
async def check_flat_energy_possibilities(
    flat: int,
    dDolya: float,
    query_api: QueryApi = Depends(get_influx_query),
) -> bool:
    all_last_target_temps_query = f"""from(bucket: "default")
    |> range(start: -3d, stop: -0s)
    |> filter(fn: (r) => r["_measurement"] == "target_temp")
    |> filter(fn: (r) => r["_field"] == "value")
    |> drop(columns: ["_measurement", "_field", "_time"])
    |> last()"""
    all_last_consumption_rates = f"""from(bucket: "default")
    |> range(start: -3d, stop: -0s)
    |> filter(fn: (r) => r["_measurement"] == "consumption")
    |> filter(fn: (r) => r["_field"] == "value")
    |> drop(columns: ["_measurement", "_field", "_time"])
    |> last()"""
    # TODO: parse queries to float arrays
    # TODO: count min_consumptions from target_temps
    # TODO: current_consumptions - min_consumptions = dCumsuctions
    # TODO: np.sum(dCumsuctions) / 6 = dNormalizedSumCumsuction
    # TODO: if dNormalizedSumCumsuction > dDolya then true else false

# @router.get("/flats/can_decrease_energy")
# async def check_flat_energy_possibilities(


# THIS SHOULD BE THE LOWEST DEFINED HANDLE
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
        case "temp" | "humd" | "curr" | "set_temp":
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
