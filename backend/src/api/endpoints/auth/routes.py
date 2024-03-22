from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.models.user import Role
from src.models.bill import Bill
from src.api.endpoints.auth.core import (
    auth_user,
    create_access_token,
    current_user,
    create_user,
    get_user_by_flat,
)
from src.schemas.auth import LoginRequest, UserResponse
from src.core.db import async_session_factory

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login_user(req: LoginRequest) -> str:
    user = await auth_user(req.name, req.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.name})
    return access_token


@router.get("/admin")
async def admin_ep(
    user: current_user(Role.ADMIN),  # type: ignore
):
    return f"Hello, admin: {user.name=}"


@router.get("/me", response_model=UserResponse)
async def get_me(
    user: current_user(),  # type: ignore
):

    return user


@router.get("/by-flat/{flat}", response_model=UserResponse)
async def get_user_info_by_flat(flat: int, user: current_user([Role.ADMIN])):  # type: ignore
    user = await get_user_by_flat(flat)

    return user


@router.post("/signup")
async def sign_up(name: str, password: str, role: str):
    if role == "admin":
        await create_user(name=name, password=password, role=Role.ADMIN)
    elif role == "user":
        await create_user(name=name, password=password, role=Role.USER)
    return 1
