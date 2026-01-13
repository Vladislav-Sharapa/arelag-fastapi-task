from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.v1 import root_validator

from app.schemas import CurrencyEnum


class UserStatusEnum(StrEnum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class UserFilter(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    status: Optional[UserStatusEnum] = None

    model_config = ConfigDict(from_attributes=True)


class RequestUserModel(BaseModel):
    email: Optional[EmailStr]


class RequestUserUpdateModel(BaseModel):
    status: UserStatusEnum


class ResponseUserBalanceModel(BaseModel):
    currency: Optional[CurrencyEnum] = None
    amount: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ResponseUserModel(BaseModel):
    id: Optional[int]
    email: Optional[str] = None
    status: Optional[UserStatusEnum] = None
    created: Optional[datetime] = None
    user_balance: Optional[List[ResponseUserBalanceModel]] = None

    model_config = ConfigDict(from_attributes=True)


class UserModel(BaseModel):
    id: Optional[int]
    email: Optional[str] = None
    status: Optional[UserStatusEnum] = None
    created: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserBalanceModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int] = None
    currency: Optional[CurrencyEnum] = None
    amount: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

    @root_validator(pre=True)
    def validate_not_negative(self, values):
        if "amount" in values and values.get("amount"):
            if values["amount"] < 0:
                raise ValueError("Amount cannot be negative")

        return values
