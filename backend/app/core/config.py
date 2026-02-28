from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    environment: str = "dev"
    database_url: str = ""
    debug: bool = False
    secret_key: str = ""
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'dev')}",
        extra="ignore",
        case_sensitive=False
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()