import os
from pathlib import Path

from fastapi_mail import ConnectionConfig
from pydantic_settings import SettingsConfigDict


class EmailSetting(ConnectionConfig):
    TEMPLATE_FOLDER: str = os.path.join(
        Path(__file__).parent.parent.resolve(), "templates"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
