from sqlalchemy.ext.asyncio import AsyncSession
from app.src.exceptions.auth_exceptions import InvalidUserPasswordException

from app.src.schemas.auth_schemas import RequestUserLoginInfoModel, TokenInfo
from app.src.utils.auth_security import verify_password
from app.src.models.user import User
from app.src.schemas.user_schemas import UserModel
from app.src.services.user import UserService
from app.src.utils.jwt import JWTHandler


class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_sevice: UserService = UserService(session)

    async def register(self):
        pass

    async def login(self, request: RequestUserLoginInfoModel) -> TokenInfo:
        user = await self.__authenticate(request.username, request.password)

        access_token = await JWTHandler.create_access_token(user)
        refresh_token = await JWTHandler.create_refresh_token(user)

        return TokenInfo(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )

    async def refresh(self, user: UserModel) -> TokenInfo:
        access_token = JWTHandler.create_access_token(user)

        return TokenInfo(access_token=access_token)

    async def __authenticate(self, email: str, password: str) -> UserModel:
        """
        Authenticate a user by verifying their email and password.

        Workflow:
            1. Retrieve the active user record from the database using the provided email.
            2. Compare the given plain-text password with the stored password hash.
            3. If the password does not match, raise InvalidUserPasswordException.
            4. If the password is valid, return a validated UserModel instance.
        Args:
            email (str): The user's email address used for login.
            password (str): The plain-text password provided by the user.
        Returns:
            UserModel: A validated user model containing the authenticated user's data.
        Raises:
            InvalidUserPasswordException: If the provided password does not match the stored hash.
            UserNotExistsException: If no user with the given email exists.
            UserAlreadyBlockedException: If the user account is blocked.
        """
        user: User = await self.user_sevice.get_active_user_by_email(email=email)
        if not verify_password(password, user.password_hash):
            raise InvalidUserPasswordException
        return UserModel.model_validate(user)
