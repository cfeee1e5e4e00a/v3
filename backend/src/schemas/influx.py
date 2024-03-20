from datetime import datetime
from dateutil import tz
from pydantic import BaseModel, ConfigDict
from influxdb_client.client.flux_table import FluxRecord


class SensorData[T](BaseModel):
    timestamp: str
    value: T

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def from_flux_record(cls, userTz: str):
        def mapper(flux_record: FluxRecord) -> "SensorData[T]":
            time: datetime = flux_record.get_time()
            time = time.replace(tzinfo=tz.tzutc()).astimezone(tz.tzutc())

            return cls(
                timestamp=time.astimezone(tz.gettz(userTz)).strftime("%H:%M"),
                value=round(flux_record.get_value(), 1),
            )

        return mapper
