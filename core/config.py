from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

settings = Settings()