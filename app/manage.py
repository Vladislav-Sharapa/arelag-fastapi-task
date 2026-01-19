import uvicorn
from fastapi import FastAPI

from app.src.api.transaction import router as transaction_router
from app.src.api.user import router as user_router
from app.src.exceptions.transaction_exceptions import register_transaction_error_handlers
from app.src.exceptions.user_exceptions import register_user_error_handlers
from app.src.core.config import config

app = FastAPI()

app.include_router(transaction_router)
app.include_router(user_router)

# Exceptions
register_transaction_error_handlers(app)
register_user_error_handlers(app)

if __name__ == "__main__":
    uvicorn.run("app.manage:app", host=config.application.APP_HOST, port=config.application.APP_PORT, reload=True)
