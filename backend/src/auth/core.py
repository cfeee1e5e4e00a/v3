from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select

from src.core.db import async_session_factory

from src.schemas.user import RoleEnum, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = '932b25ed0d90729416ba383e384567a356b2870f302fb5d04b89dc364f4ccfd6'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(name: str, password: str, roles: list[RoleEnum]):
    async with async_session_factory() as session:
        session.add(User(name=name, password_hash=get_password_hash(password), roles=roles))
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


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
