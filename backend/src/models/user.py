from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, false
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import relationship

from src.core.db import PostgresBase


class Role(Enum):
    USER_FLOOR_1 = "USER_FLOOR_1"
    USER_FLOOR_2 = "USER_FLOOR_2"
    ADMIN = "ADMIN"

    def __lt__(self, other: "Role") -> bool:
        match (self, other):
            case (Role.ADMIN, Role.USER_FLOOR_1, Role.USER_FLOOR_2):
                return True
            case _:
                return False


class User(PostgresBase):
    """
    id: int
    name: str
    password_hash: str
    flat: int
    role: Enum(ADMIN, USER_FLOOR_1, USER_FLOOR_2)
    bills: Bill[]
    """

    # TODO: add stage
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(PgEnum(Role, create_type=True), nullable=False)
    flat = Column(Integer, nullable=False)
    disabled = Column(Boolean, server_default=false(), nullable=False)
    bills = relationship("Bill", back_populates="user")
