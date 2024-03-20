from fastapi import APIRouter

from src.api.endpoints.bill.core import create_bill, Status, get_bill, get_user_bills_list, change_bill_status, \
    all_bills

router = APIRouter(prefix="/bill")


@router.post("/")
async def add_bill(amount: float, user_id: int):  # type: ignore
    return {"bill_id": await create_bill(amount=amount, status=Status.UNPAID, user_id=user_id)}


@router.get("/list")  # type: ignore
async def get_all_bills():
    return await all_bills()


# TODO: убрать pdf
@router.get("/{bill_id}")
async def get_bill_by_id(bill_id: int):
    bill = await get_bill(bill_id)
    return bill


# TODO: Скачать pdf-отчёт
@router.get("/{bill_id}/report")
async def get_bill_report(bill_id: int):
    bill = await get_bill(bill_id)
    return bill.pdf


@router.get("/users/{user_id}")
async def get_user_bill(user_id: int):
    return await get_user_bills_list(user_id)


@router.post("/{bill_id}/pay")
async def pay_for_bill(bill_id: int):
    return await change_bill_status(bill_id)
