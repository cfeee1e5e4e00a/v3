from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.core.db import Base


class LogEntry(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    note: Mapped[str] = mapped_column()
