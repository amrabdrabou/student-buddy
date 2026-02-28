from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    envirment: str = "dev"
    database_url: str
    debug: bool = False
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'dev')}",
        extra="ignore"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()