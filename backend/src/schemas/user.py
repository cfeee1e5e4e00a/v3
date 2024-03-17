from enum import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from src.core.db import Base


class RoleEnum(Enum):
    ADMIN = 'ADMIN'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    roles: list[RoleEnum] = Column(ARRAY(PgEnum(RoleEnum, create_type=True)), nullable=False, default=list())
