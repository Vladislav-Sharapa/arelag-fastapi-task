from app.src.core.exceptions import BaseHttpApplicationException
from fastapi import status


class NoResetPasswordCode(BaseHttpApplicationException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "There is no code for this email"


class InvalidResetCodeException(BaseHttpApplicationException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid reset code"


class DuplicatePasswordException(BaseHttpApplicationException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The password must not be repeated"
