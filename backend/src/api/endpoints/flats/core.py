from fastapi import Depends, APIRouter, HTTPException
from influxdb_client import QueryApi
from itertools import chain

from src.core.db import get_influx_query
from src.schemas.influx import SensorData
from src.api.endpoints.auth.core import current_user

router = APIRouter(prefix="/flats")


@router.get("/{flat}/{measurement}", response_model=list[SensorData[float]])
async def get_measurement_data(
    flat: int,
    measurement: str,
    start: str,
    stop: str,
    window: str,
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

    return map(
        SensorData[float].from_flux_record,
        filter(
            lambda x: x.get_value() is not None,
            chain.from_iterable(table.records for table in tables),
        ),
    )
