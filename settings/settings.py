from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    API_SERVER_PORT: PositiveInt
    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: SecretStr
    #: str: Postgresql database name.
    POSTGRES_DB: str


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
