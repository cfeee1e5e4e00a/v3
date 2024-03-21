
from pydantic import BaseModel


class ScheduleEntry(BaseModel):
    time: int
    temp: float


class Schedule(BaseModel):
    entries: list[ScheduleEntry]
