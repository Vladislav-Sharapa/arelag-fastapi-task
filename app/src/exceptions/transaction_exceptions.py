from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


# Custom exceptions
class TransactionNotExistsException(Exception): ...


class TransactionDoesNotBelongToUserException(Exception): ...


class CreateTransactionForBlockedUserException(Exception): ...


class UpdateTransactionForBlockedUserException(Exception): ...


class TransactionAlreadyRollbackedException(Exception): ...


# FastApi exception handlers
def register_transaction_error_hadlers(app: FastAPI):

    @app.exception_handler(CreateTransactionForBlockedUserException)
    async def create_transaction_for_blocked_user_hadler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Try to create transaction for blocked user"}
        )

    @app.exception_handler(UpdateTransactionForBlockedUserException)
    async def update_transaction_for_blocked_user_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Try to update transaction for blocked user"}
        )

    @app.exception_handler(TransactionAlreadyRollbackedException)
    async def transaction_already_rollbacked_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Transaction is already rollbacked"}
        )

    @app.exception_handler(TransactionNotExistsException)
    async def transaction_not_exists_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Transaction with this id doesn't exits"}
        )

    @app.exception_handler(TransactionDoesNotBelongToUserException)
    async def transaction_not_belong_to_user_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Transaction does not belong to user"}
        )
