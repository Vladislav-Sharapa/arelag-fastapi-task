from typing import Annotated, List
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.src.api.depedencies.user_dependencies import get_user_service
from app.src.core.config import config
from app.src.core.redis import RedisClient, get_redis_client
from app.src.exceptions.auth_exceptions import CredentialException
from app.src.schemas.auth_schemas import RequestUserLoginInfoModel, TokenTypeEnum
from fastapi import status
from app.src.models.user import User
from app.src.schemas.user_schemas import UserModel
from app.src.services.user import UserService
from app.src.utils.jwt import decode_token
from jwt import ExpiredSignatureError
from app.src.services.auth_service import AuthService
from app.src.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_auth_service(
    session: AsyncSession = Depends(get_async_session),
    redis_client: RedisClient = Depends(get_redis_client),
) -> AuthService:
    return AuthService(session=session, redis=redis_client)


async def login_attempts_dependency(
    user: RequestUserLoginInfoModel,
    redis_client: RedisClient = Depends(get_redis_client),
) -> str:
    """Dependency that checks login attempts for a given user email."""

    key = f"login_attempts:{user.username}"

    async with redis_client as storage:
        attempts = await storage.get(key)

    if attempts and int(attempts) >= config.auth.MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Try again later.",
        )
    return key


def get_current_token_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Extract and validate the payload from the current JWT token
    """
    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            detail="Signature has expired", status_code=status.HTTP_400_BAD_REQUEST
        )
    return payload


def role_required(roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if not any(role.name in roles for role in current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted"
            )
        return current_user

    return role_checker


class UserFetchFromToken:
    """
    Allows to get data from a token depending on its type.
    """

    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        user_service: UserService = Depends(get_user_service),
    ):
        await self.__validate_token_type(payload, self.token_type)
        user = await self.__get_current_auth_user(payload, user_service)
        return user

    async def __validate_token_type(self, payload: dict, token_type: str) -> None:
        current_token_type = payload.get("type")
        if current_token_type == token_type:
            return
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
        )

    async def __get_current_auth_user(
        self, payload: dict, user_service: UserService
    ) -> UserModel:
        user_id = payload.get("user_id")
        if user_id is None:
            raise CredentialException
        user: User = await user_service.get_active_user(user_id)

        return UserModel.model_validate(user)


get_current_user = UserFetchFromToken(TokenTypeEnum.ACCESS_TOKEN_TYPE)
get_current_user_for_refresh = UserFetchFromToken(TokenTypeEnum.REFRESH_TOKEN_TYPE)
