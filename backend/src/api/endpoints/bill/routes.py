from fastapi import APIRouter, HTTPException

from src.models.user import Role
from src.api.endpoints.auth.core import auth_user, create_access_token, current_user
from src.schemas.bill import AddBillRequest
from ..auth.routes import current_user
from src.api.endpoints.bill.core import create_bill, Status


router = APIRouter(prefix="/bill")


# TODO: Выставить новый счёт юзеру
@router.post("/")
async def add_bill(amount: float, user_id: int):  # type: ignore
    await create_bill(amount=amount, status=Status.UNPAID, user_id=user_id)
    return


# TODO: Получить инфу о счёте
@router.get("/{bill_id}")
async def get_bill_by_id(bill_id: int):
    pass


# TODO: Скачать pdf-отчёт
@router.get("/{bill_id}/report")
async def get_bill_report(bill_id: int):
    pass


# TODO: Получить счёта пользователя
@router.get("/users/{user_id}")
async def get_user_bill(user_id: int):
    pass


# TODO: "Оплатить" счёт
@router.post("/{bill_id}/pay")
async def pay_for_bill(bill_id: int):
    pass
