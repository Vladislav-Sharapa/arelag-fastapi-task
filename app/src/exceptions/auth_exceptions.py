from fastapi import status

from app.src.core.exceptions import BaseHttpApplicationException


class InvalidUserPasswordException(BaseHttpApplicationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect password"


class CredentialException(BaseHttpApplicationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
