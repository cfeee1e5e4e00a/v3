from pydantic import BaseModel, ConfigDict, Field
from src.models.bill import Status


class AddBillRequest(BaseModel):
    user_id: int
    amount: float
    status: Status


class BillResponse(BaseModel):
    id: int
    amount: float
    status: Status
