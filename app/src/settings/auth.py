from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSetting(BaseSettings):
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 3
    ALGORITH: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
