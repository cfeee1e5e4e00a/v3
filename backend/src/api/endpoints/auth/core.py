from typing import Annotated
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy import select
from passlib.context import CryptContext

from fastapi import Request, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from src.core.db import async_session_factory
from src.core.config import AuthSettings
from src.models.user import Role, User


api_key_header = APIKeyHeader(name="Authorization")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(name: str, password: str, role: Role, flat: int):
    async with async_session_factory() as session:
        session.add(
            User(
                name=name,
                password_hash=get_password_hash(password),
                role=role,
                flat=flat,
            )
        )
        await session.commit()


async def get_user(name: str) -> User | None:
    async with async_session_factory() as session:
        query = select(User).where(User.name == name)
        return (await session.execute(query)).scalars().first()


async def get_user_by_flat(flat: int) -> User | None:
    async with async_session_factory() as session:
        query = select(User).where(User.flat == flat)
        return (await session.execute(query)).scalars().first()


async def auth_user(name: str, password: str) -> User | None:
    user = await get_user(name)
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=AuthSettings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, AuthSettings.secret_key, algorithm=AuthSettings.algorithm
    )
    return encoded_jwt


CredentialsError = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
)


def get_current_user_wrapper(role: Role | None):
    async def get_current_user(req: Request, token=Security(api_key_header)):

        try:
            payload = jwt.decode(
                token, AuthSettings.secret_key, algorithms=[AuthSettings.algorithm]
            )
            username: str = payload.get("sub")

            if username is None:
                raise CredentialsError

        except JWTError:
            raise CredentialsError

        user = await get_user(username)

        if user is None:
            raise CredentialsError

        if role is not None and user.role < role:
            raise HTTPException(
                status_code=403,
                detail=f"Вы должны обладать как минимум ролью `{role.name}`",
            )

        return user

    return get_current_user


def current_user(role: Role | None = None) -> type[User]:
    return Annotated[str | None, Depends(get_current_user_wrapper(role))]
