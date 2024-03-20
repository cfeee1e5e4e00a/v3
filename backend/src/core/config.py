from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator
from enum import Enum
import colorlog


class ColorLogLevel(Enum):
    INFO = colorlog.INFO
    DEBUG = colorlog.DEBUG
    WARNING = colorlog.WARNING
    ERROR = colorlog.ERROR
    CRITICAL = colorlog.CRITICAL


@lambda _: _()
class AppSettings(BaseSettings):
    log_level: int

    @validator("log_level", pre=True)
    @classmethod
    def validate_log_level(cls, level: str) -> int:
        return ColorLogLevel.__members__.get(level).value

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore"
    )


@lambda _: _()
class PostgresSettings(BaseSettings):
    uri: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PG_", extra="ignore")


@lambda _: _()
class InfluxSettings(BaseSettings):
    url: str
    token: str
    org: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="INFLUX_", extra="ignore"
    )


@lambda _: _()
class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 60 * 24

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="AUTH_", extra="ignore"
    )


@lambda _: _()
class MQTTSettings(BaseSettings):
    host: str = "mqtt"
    client_id: str = "backend"
    username: str = "nti"
    password: str = "nti"

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="MQTT_", extra="ignore"
    )
