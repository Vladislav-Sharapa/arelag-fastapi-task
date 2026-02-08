from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSetting(BaseSettings):
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 3
    ALGORITH: str = "HS256"
    MAX_LOGIN_ATTEMPTS: int = 5
    BLOCK_LOGIN_TIME: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
