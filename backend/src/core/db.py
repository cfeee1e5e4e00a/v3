from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from src.core.config import PostgresSettings, InfluxSettings


async_engine = create_async_engine(PostgresSettings.uri, echo=True, echo_pool="debug")


async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session


PostgresBase = declarative_base()
InfluxClient = InfluxDBClient(
    url=InfluxSettings.url,
    token=InfluxSettings.token,
    org=InfluxSettings.org,
)


def get_influx_query():
    yield InfluxClient.query_api()


def get_influx_write():
    yield InfluxClient.write_api(write_options=SYNCHRONOUS)
