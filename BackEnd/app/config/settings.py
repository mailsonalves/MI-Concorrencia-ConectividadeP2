from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    TOKEN_EXPIRE_MIN: str = Field(..., env="TOKEN_EXPIRE_MIN")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
