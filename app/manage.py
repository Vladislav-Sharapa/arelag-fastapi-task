import uvicorn
from fastapi import FastAPI

from app.src.transactions.exceptions import register_transaction_error_hadlers
from app.src.transactions.router import router as transaction_router
from app.src.users.router import router as user_router

app = FastAPI()

app.include_router(transaction_router)
app.include_router(user_router)

register_transaction_error_hadlers(app)

if __name__ == "__main__":
    uvicorn.run("app.manage:app", host="0.0.0.0", port=7999, reload=True)
