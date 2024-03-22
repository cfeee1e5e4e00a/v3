import datetime
import io

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
from influxdb_client import QueryApi

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.endpoints.bill.core import (
    create_bill,
    Status,
    get_bill,
    get_user_bills_list,
    change_bill_status,
    all_bills,
    generate_pdf,
    make_report_user_1_floor,
    heat_cost,
    day_heats_by_range,
)
from src.schemas.bill import BillResponse
from src.core.db import get_db_session, get_influx_query
from src.models import User

router = APIRouter(prefix="/bill")


@router.post("/")
async def add_bill(
    user_id: int,
    influx_start: str,
    influx_stop: str,
    query_api: QueryApi = Depends(get_influx_query),
    session: AsyncSession = Depends(get_db_session),
):  # type: ignore
    query = select(User.flat).where(User.id == user_id)
    flat_id = (await session.execute(query)).scalars().first()
    return {
        "bill_id": await create_bill(
            amount=heat_cost(query_api, flat_id, (influx_start, influx_stop)),
            status=Status.UNPAID,
            user_id=user_id,
        )
    }


@router.get("/list")  # type: ignore
async def get_all_bills():
    bills = await all_bills()

    return (
        {"id": bill.id, "amount": bill.amount, "status": bill.status} for bill in bills
    )


@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill_by_id(bill_id: int):
    bill = await get_bill(bill_id)
    return bill


@router.get("/{bill_id}/report")
async def get_bill_report(bill_id: int):
    headers = {"Content-Disposition": f"attachment; filename={bill_id}.pdf"}
    pdf = await generate_pdf(bill_id)
    response = StreamingResponse(
        io.BytesIO(pdf), media_type="application/pdf", headers=headers
    )

    return response


# @router.get("/test_trend_report/{room}")
# async def get_test_report_1_floor(room: int, bill_id: int):
#     pdf = await make_report_user_1_floor(
#         room,
#         datetime.datetime.now(tz=datetime.timezone.utc)
#         - datetime.timedelta(minutes=15),
#         datetime.datetime.now(tz=datetime.timezone.utc),
#     )
#     headers = {"Content-Disposition": f"attachment; filename={bill_id}.pdf"}
#     response = StreamingResponse(
#         io.BytesIO(pdf), media_type="application/pdf", headers=headers
#     )
#
#     return response


@router.get("/users/{user_id}")
async def get_user_bill(user_id: int):
    return await get_user_bills_list(user_id)


@router.post("/{bill_id}/pay")
async def pay_for_bill(bill_id: int):
    return await change_bill_status(bill_id)


@router.post("/{flat_id}/energy_bill")
async def get_heat_cost(
    flat_id: int,
    influx_start: str,
    influx_stop: str,
    query_api: QueryApi = Depends(get_influx_query),
) -> float:
    return heat_cost(query_api, flat_id, (influx_start, influx_stop))


@router.post("/{flat_id}/energy_graph")
async def get_heat_cost(
    flat_id: int,
    influx_start: str,
    influx_stop: str,
    query_api: QueryApi = Depends(get_influx_query),
) -> float:
    return day_heats_by_range(query_api, flat_id, (influx_start, influx_stop)).tolist()
