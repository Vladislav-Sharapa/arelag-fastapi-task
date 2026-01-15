import uvicorn
from fastapi import FastAPI

from app.src.api.transaction import router as transaction_router
from app.src.api.user import router as user_router
from app.src.exceptions.transaction_exceptions import \
from app.src.exceptions.user_exceptions import register_user_error_handlers

app = FastAPI()

app.include_router(transaction_router)
app.include_router(user_router)

register_user_error_handlers(app)

if __name__ == "__main__":
    uvicorn.run("app.manage:app", host="0.0.0.0", port=7999, reload=True)
