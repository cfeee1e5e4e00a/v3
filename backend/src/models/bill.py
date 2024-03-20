from enum import Enum

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from src.core.db import PostgresBase


class Status(Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"


class Bill(PostgresBase):
    """
    id: int
    amount: float
    status: ENUM(PAID, UNPAID)
    pdf: bytea
    """
    __tablename__ = "bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    status = Column(PgEnum(Status, create_type=True), nullable=False)
    pdf = Column(BYTEA, nullable=True)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="bills")
