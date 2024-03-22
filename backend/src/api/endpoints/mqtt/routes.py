import json
from datetime import datetime
from numpy import exp2

from fastapi import Depends, APIRouter

from src.models import α, T_out, P_max, _FLAT_WINDOWS_SIZE
from .core import mqtt
from src.core.db import get_influx_query

router = APIRouter(prefix="/mqtt")


@router.post("/{flat}/energy_efic/yes")
def shgsgflasfjkhfhfdslkfjs(
    flat: int, dNu: float, query_api=Depends(get_influx_query)
) -> dict:
    last_current_consumption_query = f"""from(bucket: "default")
    |> range(start: -3d, stop: -0s)
    |> filter(fn: (r) => r["_measurement"] == "consumption")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["flat"] == "{flat}")
    |> drop(columns: ["_measurement", "_field", "_time", "flat"])
    |> last()"""
    cur = query_api.query(last_current_consumption_query)[0].records[0].get_value()
    mqtt.client.publish(f"/mode/{flat}", f"1 {cur-dNu}")
    return {"Code": 200}
