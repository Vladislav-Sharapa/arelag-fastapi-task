from app.src.settings.application import ApplicationSetting
from app.src.settings.auth import AuthSetting
from app.src.settings.database import PostgreSQLSetting


class Config:
    database: PostgreSQLSetting = PostgreSQLSetting()
    application: ApplicationSetting = ApplicationSetting()
    auth: AuthSetting = AuthSetting()


config = Config()
