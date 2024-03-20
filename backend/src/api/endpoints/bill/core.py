from src.core.db import async_session_factory
from src.models.bill import Bill, Status


async def create_bill(amount: float, status: Status, user_id: int):
    async with async_session_factory() as session:
        session.add(
            Bill(amount=amount, status=status, user_id=user_id)
        )
        await session.commit()
