from app.src.settings.application import ApplicationSetting
from app.src.settings.auth import AuthSetting
from app.src.settings.taskiq import TaskiqSetting
from app.src.settings.database import PostgreSQLSetting
from app.src.settings.redis import RedisSetting


class Config:
    database: PostgreSQLSetting = PostgreSQLSetting()
    application: ApplicationSetting = ApplicationSetting()
    auth: AuthSetting = AuthSetting()
    redis: RedisSetting = RedisSetting()
    taskiq: TaskiqSetting = TaskiqSetting()


config = Config()
