import secrets
import string
from fastapi.responses import JSONResponse
from fastapi import status, BackgroundTasks
from app.src.core.redis import RedisClient
from app.src.exceptions.profile import (
    InvalidResetCodeException,
    NoResetPasswordCode,
)
from app.src.schemas.auth import (
    RequestDataForResetPassword,
    RequestEmailForNotification,
)
from app.src.services.notification import NotificationService
from app.src.services.user import UserService


class RequestResetPasswordService:
    def __init__(
        self,
        user_service: UserService,
        notivication_service: NotificationService,
        redis: RedisClient,
    ):
        self.__user_service = user_service
        self.__redis = redis
        self.__notivicetion_service = notivication_service

    async def request_reset_password(
        self, request: RequestEmailForNotification, background_task: BackgroundTasks
    ) -> JSONResponse:
        key = self.__get_reset_key(request.email)

        try:
            _ = await self.__user_service.get_active_user_by_email(request.email)

            code = self.__generate_code()

            async with self.__redis as storage:
                await storage.set(key, code)

            background_task.add_task(
                self.__notivicetion_service.send,
                recepient=request,
                subject="Reset Password",
                template_body={"reset_code": code},
                template_name="email_template.html",
            )
        except Exception as e:
            print(e)
        finally:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "If your email is registered, you will receive password reset instructions"
                },
            )

    async def reset_password(
        self, request: RequestDataForResetPassword
    ) -> JSONResponse:
        key = self.__get_reset_key(request.email)

        async with self.__redis as storage:
            code = await storage.get(key)

        if not code:
            raise NoResetPasswordCode
        elif int(code) != int(request.code):
            raise InvalidResetCodeException

        user = await self.__user_service.get_active_user_by_email(request.email)

        await self.__user_service.update_password(user.id, request.password)

        async with self.__redis as storage:
            await storage.delete(key)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Password changed successfully for {request.email}"},
        )

    def __get_reset_key(self, email: str) -> str:
        return f"{email}-reset-code"

    def __generate_code(self) -> str:
        return "".join(secrets.choice(string.digits) for _ in range(6))
