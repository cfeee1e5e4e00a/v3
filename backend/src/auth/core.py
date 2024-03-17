from datetime import datetime, timedelta, timezone
from jose import jwt
from sqlalchemy import select
from passlib.context import CryptContext

from src.core.db import async_session_factory
from src.core.config import AuthSettings
from src.schemas.user import Role, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(name: str, password: str, roles: list[Role]):
    async with async_session_factory() as session:
        session.add(
            User(name=name, password_hash=get_password_hash(password), roles=roles)
        )
        await session.commit()


async def get_user(name: str) -> User | None:
    async with async_session_factory() as session:
        query = select(User).where(User.name == name)
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
