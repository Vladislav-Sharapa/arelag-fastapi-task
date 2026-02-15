from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSetting(BaseSettings):
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: str = 6380
    TTL: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
