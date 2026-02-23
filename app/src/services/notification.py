from abc import ABC, abstractmethod

from fastapi_mail import FastMail, MessageSchema, MessageType

from app.src.schemas.auth import RequestEmailForNotification


class BaseMailService(ABC):
    @abstractmethod
    async def send(self, recepients: str):
        pass


class NotificationService(BaseMailService):
    def __init__(self, mail_serice: FastMail):
        self.__service = mail_serice

    async def send(
        self,
        recepient: RequestEmailForNotification,
        subject: str,
        template_body: dict,
        template_name: str,
    ) -> None:
        msg = MessageSchema(
            subject=subject,
            recipients=[
                recepient.email,
            ],
            subtype=MessageType.html,
            template_body=template_body,
        )

        await self.__service.send_message(msg, template_name=template_name)
