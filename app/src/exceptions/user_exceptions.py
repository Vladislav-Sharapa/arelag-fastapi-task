from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.src.core.exceptions import BaseHttpApplicationException


class UserAlreadyExistsException(Exception): ...


class UserNotExistsException(Exception): ...


class UserAlreadyBlockedException(Exception): ...


class UserAlreadyActiveException(Exception): ...


class NegativeBalanceException(Exception): ...


class UserBalanceNotFound(BaseHttpApplicationException): ...


# FastAPI exception handlers
def register_user_error_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": "User with this email already exists"}
        )

    @app.exception_handler(UserNotExistsException)
    async def user_not_exists_handler(request, exc):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User does not exist"})

    @app.exception_handler(UserAlreadyBlockedException)
    async def user_blocked_handler(request, exc):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "User is already blocked"})

    @app.exception_handler(UserAlreadyActiveException)
    async def user_active_handler(request, exc):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "User is already active"})

    @app.exception_handler(NegativeBalanceException)
    async def negative_balance_handler(request, exc):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Negative balance"})

    @app.exception_handler(UserBalanceNotFound)
    async def balance_not_found_handler(request, exc):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "User balance was not found"})
