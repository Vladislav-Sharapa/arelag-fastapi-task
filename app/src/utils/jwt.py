from datetime import timedelta, datetime, timezone

from typing import Any, Dict, Optional
import uuid
import jwt

from app.src.core.config import config
from app.src.schemas.auth_schemas import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenTypeEnum,
)
from app.src.schemas.user_schemas import UserModel


def encode_token(
    data: dict, expire_minutes: int, expire_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, jti=str(uuid.uuid4()))

    encoded_jwt = jwt.encode(
        to_encode, config.auth.SECRET, algorithm=config.auth.ALGORITH
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode JWT token
    """
    payload: dict = jwt.decode(token, config.auth.SECRET, config.auth.ALGORITH)
    return payload


class JWTHandler:
    @staticmethod
    async def __create_token(
        token_type: str,
        token_data: dict,
        expire_minutes: int = config.auth.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {"type": token_type}
        jwt_payload.update(token_data)
        return encode_token(
            data=jwt_payload,
            expire_minutes=expire_minutes,
            expire_delta=expire_timedelta,
        )

    @staticmethod
    async def create_access_token(user: UserModel) -> str:
        jwt_payload = AccessTokenPayload(
            sub=user.email, email=user.email, user_id=user.id
        )
        token = await JWTHandler.__create_token(
            token_type=TokenTypeEnum.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload.model_dump(),
            expire_minutes=config.auth.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return token

    @staticmethod
    async def create_refresh_token(user: UserModel) -> str:
        jwt_payload = RefreshTokenPayload(sub=user.email, user_id=user.id)
        token = await JWTHandler.__create_token(
            token_type=TokenTypeEnum.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload.model_dump(),
            expire_timedelta=timedelta(days=config.auth.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return token
