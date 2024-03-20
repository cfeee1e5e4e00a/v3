from fastapi import Depends, APIRouter
from influxdb_client import QueryApi
from itertools import chain

from src.core.db import get_influx_query
from src.schemas.influx import SensorData

router = APIRouter(prefix="/flats")


@router.get("/{id}/temp", response_model=list[SensorData[float]])
async def get_temperatures(
    id: int, period: str, query_api: QueryApi = Depends(get_influx_query)
):
    query = f"""from(bucket: "default")\
    |> range(start: -{period})\
    |> filter(fn: (r) => r["_measurement"] == "temp")\
    |> filter(fn: (r) => r["_field"] == "value")\
    |> yield(name: "last")"""

    tables = query_api.query(query)

    return map(
        SensorData[float].from_flux_record,
        chain.from_iterable(table.records for table in tables),
    )
