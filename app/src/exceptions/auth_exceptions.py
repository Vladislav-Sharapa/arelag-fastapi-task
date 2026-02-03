from fastapi import HTTPException, status


class InvalidUserPasswordException(HTTPException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = ("Incorrect password",)


class CredentialException(HTTPException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = ("Could not validate credentials",)
