from fastapi import Depends, APIRouter
from influxdb_client import QueryApi
from src.core.db import get_influx_query

router = APIRouter(prefix="/flats")


@router.get("/{id}/temp")
async def root(id: int, period: str, query_api: QueryApi = Depends(get_influx_query)):
    query = f"""from(bucket: "default")\
    |> range(start: -{period})\
    |> filter(fn: (r) => r["_measurement"] == "temp")\
    |> filter(fn: (r) => r["_field"] == "value")\
    |> yield(name: "last")"""

    obj = query_api.query(query)

    print(obj, type(obj), f"{obj!r}")
    print(dir(obj))

    return obj
