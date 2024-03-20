from pydantic import BaseModel, ConfigDict
from datetime import datetime
from influxdb_client.client.flux_table import FluxRecord
import time


class SensorData[T](BaseModel):
    timestamp: int
    value: T

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def from_flux_record(cls, flux_record: FluxRecord) -> "SensorData[T]":
        return cls(
            timestamp=int(flux_record.get_time().timestamp()),
            value=flux_record.get_value(),
        )
