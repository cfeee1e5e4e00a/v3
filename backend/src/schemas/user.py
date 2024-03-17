from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.core.db import PostgresBase


class Role(Enum):
    ADMIN = "ADMIN"


class User(PostgresBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    roles: list[Role] = Column(
        ARRAY(PgEnum(Role, create_type=True)), nullable=False, default=list()
    )
