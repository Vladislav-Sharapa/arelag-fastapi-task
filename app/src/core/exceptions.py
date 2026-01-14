from fastapi import HTTPException, status


class BaseHttpApplicationException(HTTPException):
    status_code: int | None = None
    detail: str | None = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BadRequestDataException(BaseHttpApplicationException):
    status_code = (status.HTTP_422_UNPROCESSABLE_ENTITY,)
    detail = "Unprocessable data in request"
