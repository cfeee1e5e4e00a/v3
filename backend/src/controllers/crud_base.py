from dataclasses import dataclass
from sqlalchemy import any_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.core.logger import logger
from pydantic import BaseModel


logger.debug("Init base CRUD")


@dataclass
class BaseCRUD:
    """Base CRUD class"""

    model: DeclarativeBase  # Any SQLAlchemy model class

    async def get(
        self,
        session: AsyncSession,
        _id: int,
    ):
        """Get object by id"""

        logger.info("Get object from CRUDBase")

        db_obj = (
            await session.querry(self.model)
            .select(self.model)
            .where(self.model.id == _id)
        )

        db_obj = db_obj.scalars()

        logger.info("Get object from CRUDBase finished")

        return db_obj.first()

    async def get_all(self, session: AsyncSession, *, _id: int | list[int] = tuple()):
        """Get all objects"""

        logger.info("Get all object from CRUDBase")

        if isinstance(_id, int):
            _filter = self.model.id == _id
        else:
            ids = _id
            _filter = any_(*[self.model.id == _id for _id in ids])

        db_objs = await session.querry(self.model).select(self.model).where(_filter)
        db_objs = db_objs.scalars()

        logger.info("Get all objects from CRUDBase finished")

        return db_objs.all()

    async def insert(self, session: AsyncSession, data: list[BaseModel]):
        data: list[dict] = [row.model_dump() for row in data]

        session.querry(self.model).add(data)
        session.commit()


logger.debug("Finish init base CRUD")
