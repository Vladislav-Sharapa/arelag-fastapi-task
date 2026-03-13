from fastapi import Depends

from app.src.api.depedencies.email import get_fast_mail_notification_service
from app.src.api.depedencies.user_dependencies import get_user_service
from app.src.core.config import config
from app.src.core.redis import get_redis_client
from app.src.services.auth.profile import RequestResetPasswordService


def get_request_reset_password_service(
    user_service=Depends(get_user_service),
    notivication_service=Depends(get_fast_mail_notification_service),
    redis=Depends(get_redis_client(config.redis.TTL_PASSWORD_RESET_CODE)),
):
    return RequestResetPasswordService(
        user_service=user_service,
        notivication_service=notivication_service,
        redis=redis,
    )
