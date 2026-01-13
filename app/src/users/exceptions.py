from fastapi import HTTPException, status

from app.exceptions import BaseHttpApplicationException


class UserAlreadyExistsException(BaseHttpApplicationException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this email already exists"


class UserNotExistsException(BaseHttpApplicationException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User does not exist"


class UserAlreadyBlockedException(BaseHttpApplicationException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User is already blocked"


class UserAlreadyActiveException(BaseHttpApplicationException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User is already active"


class NegativeBalanceException(HTTPException): ...
