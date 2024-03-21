from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from src.core.db import PostgresBase


class TempScheduleEntry(PostgresBase):
    __tablename__ = 'temp_schedule'

    fucking_unneeded_pk = Column(Integer, primary_key=True, autoincrement=True)
    flat = Column(Integer)
    start_time = Column(DateTime)
    was_sent = Column(Boolean)
    start_offset = Column(Integer)
    end_offset = Column(Integer)
    # time_offset = Column(Integer)  # offset from start time in seconds
    target_temp = Column(Float)
