from fastapi import APIRouter, HTTPException


from src.models.user import Role
from src.api.endpoints.auth.core import auth_user, create_access_token, current_user
from src.schemas.login import LoginRequest

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


@router.get("/me")
async def get_me(
    user: current_user(),  # type: ignore
):
    return f"Hello, {user.name}, your roles are {user.roles}"
