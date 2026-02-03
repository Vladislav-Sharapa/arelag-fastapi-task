from typing import Annotated, List
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.src.api.depedencies.user_dependencies import get_user_service
from app.src.exceptions.auth_exceptions import CredentialException
from app.src.schemas.auth_schemas import TokenTypeEnum
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


def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(session=session)


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
            raise CredentialException  # TODO
        user: User = await user_service.get_active_user(user_id)

        return UserModel.model_validate(user)


get_current_user = UserFetchFromToken(TokenTypeEnum.ACCESS_TOKEN_TYPE)
get_current_user_for_refresh = UserFetchFromToken(TokenTypeEnum.REFRESH_TOKEN_TYPE)
