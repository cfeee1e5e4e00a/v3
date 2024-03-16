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
class KeyCloakSettings(BaseSettings):
    url: str
    realm: str
    client_id: str
    client_secret: str
    login_callback_uri: str
    logout_callback_uri: str

    # @validator("*", pre=True)
    # @classmethod
    # def validate_log_level(cls, _input: str) -> str:
    #     return f'"{_input}"'

    model_config = SettingsConfigDict(env_file=".env", env_prefix="KC_", extra="ignore")
