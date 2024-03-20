from fastapi import APIRouter, HTTPException

from src.models.user import Role
from src.api.endpoints.auth.core import auth_user, create_access_token, current_user
from src.schemas.bill import AddBillRequest
from ..auth.routes import current_user
from src.api.endpoints.bill.core import create_bill, Status


router = APIRouter(prefix="/bill")


@router.get('/{id}')
async def get_bill():
    pass


@router.post("/")
async def add_bill(amount: float, status: Status, user_id: int, user: current_user()):
    await create_bill(amount=amount, status=status, user_id=user_id)
    return

