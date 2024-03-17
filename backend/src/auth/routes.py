from datetime import timedelta
from typing import Annotated, TypeAlias

from fastapi import APIRouter, Request, Depends, HTTPException
from jose import jwt, JWTError

from src.schemas.user import RoleEnum, User

router = APIRouter(prefix="/auth")
from pydantic import BaseModel
from src.auth.core import auth_user, create_access_token, SECRET_KEY, ALGORITHM, get_user


class LoginRequest(BaseModel):
    name: str
    password: str





def get_current_user_wrapper(role: RoleEnum | None):
    async def get_current_user(req: Request):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )
        key = 'Authorization'
        token = req.headers.get(key, '')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await get_user(username)
        if user is None:
            raise credentials_exception
        if role is not None and role not in user.roles:
            raise HTTPException(
                status_code=403,
                detail=f"You do not have required role: {role}"
            )
        return user
    return get_current_user


def current_user(role: RoleEnum | None = None) -> type[User]:
    return Annotated[str|None, Depends(get_current_user_wrapper(role))]


@router.post("/login")
async def login_user(req: LoginRequest) -> str:
    user = await auth_user(req.name, req.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password'
        )
    access_token = create_access_token(
        data={"sub": user.name}
    )
    return access_token


@router.get("/admin")
async def admin_ep(user: current_user(RoleEnum.ADMIN)):
    return f'Hello, admin: {user.name=}'


@router.get("/me")
async def get_me(user: current_user()):
    return f'Hello, {user.name}, your roles are {user.roles}'

