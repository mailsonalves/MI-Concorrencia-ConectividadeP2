from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    DB_URL: str = Field(default="sqlite+aiosqlite:///database.db")


settings = Settings()
