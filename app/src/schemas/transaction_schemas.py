import typing
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from app.src.core.enums import CurrencyEnum


class TransactionStatusEnum(StrEnum):
    processed = "PROCESSED"
    roll_backed = "ROLLBACKED"


class RequestTransactionModel(BaseModel):
    currency: CurrencyEnum
    amount: Decimal


class ResponseTransactionModel(BaseModel):
    pass


class TransactionModel(BaseModel):
    id: typing.Optional[int]
    user_id: typing.Optional[int] = None
    currency: typing.Optional[CurrencyEnum] = None
    amount: typing.Optional[float] = None
    status: typing.Optional[TransactionStatusEnum] = None
    created: typing.Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
