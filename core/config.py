from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    echo: bool = False

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  


class JWTSettings(BaseSettings):
    private_key_path: str
    public_key_path: str
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore") 


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    jwt: JWTSettings = JWTSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore") 


settings = Settings()
