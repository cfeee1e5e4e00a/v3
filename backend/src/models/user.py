from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.core.db import PostgresBase


class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

    def __lt__(self, other: "Role") -> bool:
        match (self, other):
            case (Role.USER, Role.ADMIN):
                return True
            case _:
                return False


class User(PostgresBase):
    """
    id: int
    name: str
    password_hash: str
    role: Enum(ADMIN, USER)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(PgEnum(Role, create_type=True), nullable=False)
