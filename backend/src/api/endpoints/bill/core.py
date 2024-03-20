from src.core.db import async_session_factory
from src.models.bill import Bill, Status
from sqlalchemy import select, update
from math import log2, e

type m2 = float
type m3 = float

α = 20  # window heat transfer coef
dQ_to_V = 350.722  # heat per logarifmic ration of temperatures per volume

_SIDE_WINDOWS_SIZE: m2 = 0.0093
_CENTRAL_WINDOWS_SIZE: m2 = 0.0057
_FLAT_WINDOWS_SIZE: dict[int, m2] = {
    1: _SIDE_WINDOWS_SIZE,
    2: _CENTRAL_WINDOWS_SIZE,
    3: _SIDE_WINDOWS_SIZE,
    4: _SIDE_WINDOWS_SIZE,
    5: _CENTRAL_WINDOWS_SIZE,
    6: _SIDE_WINDOWS_SIZE,
}

_SECOND_FLOOR_FLAT_VOLUME: m3 = 0.002
_FIRST_FLOOR_FLAT_VOLUME: m3 = 0.00225
_FLAT_VOLUME: dict[int, m3] = {
    1: _SECOND_FLOOR_FLAT_VOLUME,
    2: _SECOND_FLOOR_FLAT_VOLUME,
    3: _SECOND_FLOOR_FLAT_VOLUME,
    4: _FIRST_FLOOR_FLAT_VOLUME,
    5: _FIRST_FLOOR_FLAT_VOLUME,
    6: _FIRST_FLOOR_FLAT_VOLUME,
}


async def create_bill(amount: float, status: Status, user_id: int):
    bill = Bill(amount=amount, status=status, user_id=user_id)
    async with async_session_factory() as session:
        session.add(bill)
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


def stabilization_cost(flat_id: int, dT: float, dt: float) -> float:
    return α * _FLAT_WINDOWS_SIZE.get(flat_id, _CENTRAL_WINDOWS_SIZE) * dt * dT


async def heat_cost_on_period(flat_id: int, T_in: float, T_in_previous: float) -> float:
    return (
        dQ_to_V
        * _FLAT_VOLUME.get(flat_id, _SECOND_FLOOR_FLAT_VOLUME)
        * log2(T_in / T_in_previous)
        / log2(e)
    )
