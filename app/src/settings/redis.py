from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSetting(BaseSettings):
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: str = 6380
    TTL_PASSWORD_ATTEMPS: int = 3600
    TTL_PASSWORD_RESET_CODE: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
