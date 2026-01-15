from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSetting(BaseSettings):
    APP_HOST: str = "localhost"
    APP_PORT: int = 7999

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
