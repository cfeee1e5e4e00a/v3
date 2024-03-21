from pydantic import BaseModel, ConfigDict, Field
from src.models.user import Role


class LoginRequest(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    role: Role
    flat: int
    disabled: bool

    model_config = ConfigDict(
        extra="ignore", populate_by_name=True, use_enum_values=False
    )
