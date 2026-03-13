from fastapi_mail import FastMail
from app.src.core.config import config
from app.src.services.notification import NotificationService


def get_fast_mail_notification_service() -> FastMail:
    return NotificationService(FastMail(config=config.email))
