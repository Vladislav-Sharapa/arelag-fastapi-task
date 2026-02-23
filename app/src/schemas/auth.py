from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TokenTypeEnum(StrEnum):
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


class RoleEnum(StrEnum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class TokenData(BaseModel):
    user_uuid: int


class AccessTokenPayload(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenPayload(BaseModel):
    sub: Optional[str] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class RequestUserLoginInfoModel(BaseModel):
    username: str
    password: str
