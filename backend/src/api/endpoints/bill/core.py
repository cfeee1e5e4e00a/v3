from src.core.db import async_session_factory
from src.models.bill import Bill, Status
from sqlalchemy import select, update


async def create_bill(amount: float, status: Status, user_id: int):
    bill = Bill(amount=amount, status=status, user_id=user_id)
    async with async_session_factory() as session:
        session.add(
            bill
        )
        await session.commit()
        return bill.id


async def get_bill(id: int):
    async with async_session_factory() as session:
        query = select(Bill).where(Bill.id == id)
        return (await session.execute(query)).scalars().first()


async def get_user_bills_list(user_id: int):
    async with async_session_factory() as session:
        query = select(Bill).where(Bill.user_id == user_id)
        return (await session.execute(query)).scalars().all()


async def change_bill_status(id: int):
    async with async_session_factory() as session:
        query = select(Bill).where(Bill.id == id)
        bill = (await session.execute(query)).scalars().first()
        bill.status = Status.PAID
        await session.commit()
        return {"bill_id": id}
