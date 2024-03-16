from dataclasses import dataclass
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import logger

logger.debug("Init base CRUD")


@dataclass
class BaseCRUD:
    """Base CRUD class"""

    model: Any  # Any SQLAlchemy model class

    async def get(
        self,
        session: AsyncSession,
        obj_id: int,
    ):
        """Get object by id"""

        logger.info("Get object from CRUDBase")
        db_obj = await session.scalars(
            select(self.model).where(self.model.id == obj_id)
        )
        logger.info("Get object from CRUDBase finished")
        return db_obj.first()

    async def get_all(self, session: AsyncSession):
        """Get all objects"""

        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Update object"""

        logger.info("Update object from CRUDBase")
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        logger.info("Update object from CRUDBase finished")
        return db_obj


logger.debug("Finish init base CRUD")
