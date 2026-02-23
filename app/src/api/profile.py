from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from app.src.api.depedencies.profile import get_request_reset_password_service
from app.src.schemas.auth import (
    RequestDataForResetPassword,
    RequestEmailForNotification,
)
from app.src.services.auth.profile import RequestResetPasswordService


router = APIRouter(
    prefix="/profile",
    tags=[
        "profile",
    ],
)


@router.post("/request-password-reset")
async def request_reset_password(
    request: RequestEmailForNotification,
    background_task: BackgroundTasks,
    request_reset_password_service: RequestResetPasswordService = Depends(
        get_request_reset_password_service
    ),
) -> JSONResponse:
    response = await request_reset_password_service.request_reset_password(
        request, background_task
    )

    return response


@router.post("/reset-password")
async def reset_password(
    request: RequestDataForResetPassword,
    request_reset_password_service: RequestResetPasswordService = Depends(
        get_request_reset_password_service
    ),
) -> JSONResponse:
    response = await request_reset_password_service.reset_password(request)

    return response
